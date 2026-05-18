from agents.common.geometry import GeometryFunctions
from politics.states.state import State
from schemas.geometry import GeometryConfig
from schemas.params import ParamsConfig


def map_state_2_state_idx(state: State, geometry: GeometryConfig, params: ParamsConfig) -> int:
    """"""
    qstate = GeometryFunctions.get_quant(
        state=state, geometry=geometry, params=params
    )
    x, y, b, v = params.agent.quants.x, params.agent.quants.y, params.agent.quants.b, params.agent.quants.v
    state_idx = ((qstate.v * b + qstate.b) * y + qstate.y) * x + qstate.x
    return state_idx
