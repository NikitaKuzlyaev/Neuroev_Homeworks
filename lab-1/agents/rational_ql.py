from agents.agent import Agent
from agents.common.agent_spawner import AgentSpawner
from agents.common.geometry import GeometryFunctions
from bootstraps.key_registry import StorageKey
from framework.context import Context
from mixins.degradational import Degradational
from politics.politic import Politic
from politics.states.state import State
from politics.table import Table
from schemas.action import Action
from schemas.agent import StepResponse
from schemas.geometry import GeometryConfig
from schemas.params import ParamsConfig


class RationalQleaningAgent(Agent):

    def __init__(self, state: State, context: Context, politic: Politic, table: Table, gamma: float = 0.99,
                 alpha: float = 0.1):
        """"""
        super().__init__(state, context, politic, table)
        self.state = state
        self._context = context
        self._politic = politic
        self._table = table
        self._gamma = gamma
        self._alpha = alpha
        self.action_list: list[Action] = context.get(StorageKey.ACTION.value).actions
        self._geometry: GeometryConfig = context.get(StorageKey.GEO.value)
        self._params: ParamsConfig = context.get(StorageKey.PARAMS.value)

    def step(self) -> StepResponse:
        """"""
        old_state_idx = self._map_state_2_state_idx(state=self.state, geometry=self._geometry, params=self._params)
        action_idx = self._politic.make_action(
            table=self._table,
            state_idx=old_state_idx,
            n_actions=len(self.action_list) // 4 * 3,
        )
        action = self.action_list[action_idx]
        return StepResponse(action=action, old_state_idx=old_state_idx)

    def propagate(self, old_state: State, new_state: State, action: Action, reward: float, done: bool = False) -> None:
        """"""
        old_state_idx = self._map_state_2_state_idx(state=old_state, geometry=self._geometry, params=self._params)
        new_state_idx = self._map_state_2_state_idx(state=new_state, geometry=self._geometry, params=self._params)

        action_idx = self.action_list.index(action)
        old_q = self._table.get(old_state_idx, action_idx)

        if done:
            target = reward
        else:
            best_next_action_idx = self._table.best_action(new_state_idx)
            best_next_q = self._table.get(new_state_idx, best_next_action_idx)
            target = reward + self._gamma * best_next_q

        new_value = old_q + self._alpha * (target - old_q)
        self._table.set(old_state_idx, action_idx, new_value)

    def reset(self) -> None:
        """"""
        x, y = AgentSpawner.get_spawn_point(self._context.get(StorageKey.GEO.value))
        state = State(x=x, y=y, b=self._params.agent.battery.max_value, v=0.0)
        self.state = state

        if isinstance(self._politic, Degradational):
            self._politic.degradation()
