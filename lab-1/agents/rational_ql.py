from agents.agent import Agent
from agents.common.agent_spawner import AgentSpawner
from agents.common.geometry import GeometryFunctions
from bootstraps.key_registry import StorageKey
from framework.context import Context
from politics.politic import Politic
from politics.states.state import State
from politics.table import Table
from schemas.geometry import GeometryConfig
from schemas.params import ParamsConfig


class RationalQleaningAgent(Agent):

    def __init__(self, state: State, context: Context, politic: Politic, table: Table):
        self.state = state
        self.context = context
        self.politic = politic
        self.table = table

        self.action_list = context.get(StorageKey.ACTION.value).actions

    def step(self):
        state_idx = self._map_state_2_state_idx()


        best_action_idx = self.table.best_action(state_idx=state_idx)
        best_action = self.action_list[best_action_idx]

        print("best", best_action_idx)
        print("actions", best_action)

    def reset(self) -> None:
        x, y = AgentSpawner.get_spawn_point(self.context.get(StorageKey.GEO.value))
        print(x, y)
        state = State(x=x, y=y, b=0.0, v=0.0)
        self.state = state

    def propagate(self):
        pass

    def _map_state_2_state_idx(self) -> int:
        geometry: GeometryConfig = self.context.get(StorageKey.GEO.value)
        params: ParamsConfig = self.context.get(StorageKey.PARAMS.value)

        qstate = GeometryFunctions.get_quant(
            state=self.state, geometry=geometry, params=params)

        x, y, b, v = params.agent.quants.x, params.agent.quants.y, params.agent.quants.b, params.agent.quants.v
        return ((qstate.v * b + qstate.b) * y + qstate.y) * x + qstate.x
