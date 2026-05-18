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


class ProspectTheoryQleaningAgent(Agent):

    def __init__(
            self, state: State, context: Context, politic: Politic, table: Table, gamma: float = 0.99,
            lr: float = 0.9, alpha: float = 0.88, beta: float = 0.88, lambda_: float = 2.35
    ):
        """"""
        super().__init__(state, context, politic, table)
        self.state = state
        self._context = context
        self._politic = politic
        self._table = table
        self._gamma = gamma
        self._lr = lr
        self._alpha = alpha
        self._beta = beta
        self._lambda = lambda_
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
            self, old_state: State, new_state: State, action: Action, reward: float, done: bool = False
    ) -> None:
        """"""
        old_state_idx = map_state_2_state_idx(state=old_state, geometry=self._geometry, params=self._params, )
        new_state_idx = map_state_2_state_idx(state=new_state, geometry=self._geometry, params=self._params, )

        action_idx = self.action_list.index(action)
        old_q = self._table.get(old_state_idx, action_idx)

        subjective_reward = self._prospect_value(reward)

        if done:
            target = subjective_reward
        else:
            best_next_action_idx = self._table.best_action(new_state_idx)
            best_next_q = self._table.get(new_state_idx, best_next_action_idx)
            target = subjective_reward + self._gamma * best_next_q

        td_error = target - old_q
        new_value = old_q + self._lr * td_error

        self._table.set(old_state_idx, action_idx, new_value)

    def _prospect_value(
            self, reward: float
    ) -> float:
        """"""
        if reward >= 0:
            return reward ** self._alpha

        return -self._lambda * ((-reward) ** self._beta)

    def reset(self) -> None:
        """"""
        x, y = AgentSpawner.get_spawn_point(
            self._context.get(StorageKey.GEO.value),
        )
        state = State(
            x=x, y=y, b=self._params.agent.battery.max_value, v=0.0,
        )
        self.state = state
