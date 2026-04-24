import math

from agents.common.wind import WindManager
from politics.states.state import State
from rules.charge import is_inside_charge_area
from schemas.action import Action
from schemas.geometry import GeometryConfig
from schemas.params import ParamsConfig


def get_new_xy(
        state: State, action: Action, wind_manager: WindManager
) -> tuple[float, float]:
    """"""
    x = state.x + action.speed.value * math.cos(action.direction.radians) + wind_manager.wx
    y = state.y + action.speed.value * math.sin(action.direction.radians) + wind_manager.wy
    return x, y


def get_new_b(
        state: State, params: ParamsConfig, geometry: GeometryConfig, wind_manager: WindManager
) -> float:
    """"""
    _I = int(is_inside_charge_area(state=state, geometry=geometry))

    speed_coef = params.agent.battery.speed_coef
    wind_x_coef = params.agent.battery.wind_x_coef
    wind_y_coef = params.agent.battery.wind_y_coef
    charge_coef = params.agent.battery.charge_coef
    wx = wind_manager.wx
    wy = wind_manager.wy

    b = min(1.0,
            state.b + speed_coef * state.v ** 2 + wind_x_coef * abs(wx) + wind_y_coef * abs(wy) + _I * charge_coef)
    return b
