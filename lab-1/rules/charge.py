import math

from politics.states.state import State
from schemas.geometry import GeometryConfig


def is_inside_charge_area(state: State, geometry: GeometryConfig) -> bool:
    print((geometry.target.x, geometry.target.y), (state.x, state.y), math.dist(
        (state.x, state.y),
        (geometry.target.x, geometry.target.y)
    ))
    I = math.dist(
        (state.x, state.y),
        (geometry.target.x, geometry.target.y)
    ) < geometry.target.r
    return I
