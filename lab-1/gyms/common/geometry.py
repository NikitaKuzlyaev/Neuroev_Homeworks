from politics.states.quant_state import QuantState
from politics.states.state import State
from schemas.geometry import GeometryConfig
from schemas.params import ParamsConfig
from utils.math_funcs import MathFunctions


class GeometryFunctions:

    @staticmethod
    def get_quant(state: State, geometry: GeometryConfig, params: ParamsConfig) -> QuantState:
        qx = GeometryFunctions._quant_value(
            state.x, geometry.borders.min_x, geometry.borders.max_x, params.agent.quants.x)

        qy = GeometryFunctions._quant_value(
            state.y, geometry.borders.min_y, geometry.borders.max_y, params.agent.quants.y)

        qb = GeometryFunctions._quant_value(
            state.b, params.agent.battery.min_value, params.agent.battery.max_value, params.agent.quants.b)

        qv = GeometryFunctions._quant_value(
            state.v, params.agent.speed.min_value, params.agent.speed.max_value, params.agent.quants.v)

        return QuantState(x=qx, y=qy, b=qb, v=qv)

    @staticmethod
    def _quant_value(value, v_min, v_max, quants):
        value = MathFunctions.clip(value, v_min, v_max)

        if quants <= 1:
            return 0

        if value == v_max:
            return quants - 1

        quant_size = v_max - v_min
        value = (value - v_min) / (quant_size / quants)
        return int(value)
