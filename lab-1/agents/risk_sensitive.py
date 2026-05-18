import math

from agents.agent import Agent
from agents.common.agent_spawner import AgentSpawner
from bootstraps.key_registry import StorageKey
from framework.context import Context
from politics.politic import Politic
from politics.states.state import State
from politics.table import Table
from schemas.action import Action
from schemas.agent import StepResponse
from schemas.geometry import GeometryConfig
from schemas.params import ParamsConfig
from utils.state import map_state_2_state_idx


class RiskSensitiveQleaningAgent(Agent):

    def __init__(
            self, state: State, context: Context, politic: Politic, table: Table,
            gamma: float = 0.99, learning_rate: float = 0.9, eta: float = 2.0, eta_eps: float = 1e-8,
    ):
        """"""
        super().__init__(state, context, politic, table)
        self.state = state
        self._context = context
        self._politic = politic
        self._table = table

        self._gamma = gamma
        self._learning_rate = learning_rate
        self._eta = eta
        self._eta_eps = eta_eps

        self.action_list: list[Action] = context.get(StorageKey.ACTION.value).actions
        self._geometry: GeometryConfig = context.get(StorageKey.GEO.value)
        self._params: ParamsConfig = context.get(StorageKey.PARAMS.value)

    def step(self) -> StepResponse:
        """"""
        old_state_idx = map_state_2_state_idx(state=self.state, geometry=self._geometry, params=self._params, )

        action_idx = self._politic.make_action(
            table=self._table,
            state_idx=old_state_idx,
            n_actions=len(self.action_list) // 4 * 3,
        )

        action = self.action_list[action_idx]

        return StepResponse(action=action, old_state_idx=old_state_idx)

    def propagate(
            self, old_state: State, new_state: State, action: Action, reward: float, done: bool = False,
    ) -> None:
        """"""
        old_state_idx = map_state_2_state_idx(state=old_state, geometry=self._geometry, params=self._params, )
        new_state_idx = map_state_2_state_idx(state=new_state, geometry=self._geometry, params=self._params, )

        action_idx = self.action_list.index(action)
        old_q = self._table.get(old_state_idx, action_idx)

        if abs(self._eta) < self._eta_eps:
            self._propagate_risk_neutral(
                old_state_idx=old_state_idx,
                new_state_idx=new_state_idx,
                action_idx=action_idx,
                old_q=old_q,
                reward=reward,
                done=done,
            )
            return

        old_u = self._q_to_u(old_q)

        if done:
            target_u = self._q_to_u(reward)
        else:
            best_next_action_idx = self._table.best_action(new_state_idx)
            best_next_q = self._table.get(new_state_idx, best_next_action_idx)

            target_log_u = -self._eta * reward + self._gamma * self._q_to_log_u(best_next_q)
            target_u = math.exp(target_log_u)

        new_u = (1.0 - self._learning_rate) * old_u + self._learning_rate * target_u
        new_q = self._u_to_q(new_u)

        self._table.set(old_state_idx, action_idx, new_q)

    def reset(self) -> None:
        """"""
        x, y = AgentSpawner.get_spawn_point(
            self._context.get(StorageKey.GEO.value),
        )
        state = State(
            x=x, y=y, b=self._params.agent.battery.max_value, v=0.0,
        )
        self.state = state

    def _propagate_risk_neutral(
            self, old_state_idx: int, new_state_idx: int, action_idx: int, old_q: float, reward: float,
            done: bool = False,
    ) -> None:
        """"""
        if done:
            target = reward
        else:
            best_next_action_idx = self._table.best_action(new_state_idx)
            best_next_q = self._table.get(new_state_idx, best_next_action_idx)
            target = reward + self._gamma * best_next_q

        new_q = old_q + self._learning_rate * (target - old_q)

        self._table.set(old_state_idx, action_idx, new_q)

    def _q_to_u(self, q_value: float) -> float:
        """"""
        return math.exp(self._q_to_log_u(q_value))

    def _q_to_log_u(self, q_value: float) -> float:
        """"""
        return -self._eta * q_value

    def _u_to_q(self, u_value: float) -> float:
        """"""
        safe_u_value = max(u_value, 1e-300)
        return -math.log(safe_u_value) / self._eta
