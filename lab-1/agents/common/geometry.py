from politics.states.quant_state import QuantState
from politics.states.state import State
from schemas.geometry import (
    GeometryConfig,
    RectangleObstacle,
)
from schemas.params import ParamsConfig
from utils.math_funcs import MathFunctions


class GeometryFunctions:

    @staticmethod
    def get_quant(state: State, geometry: GeometryConfig, params: ParamsConfig) -> QuantState:
        """"""

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
    def get_next_position(
            x1: float, y1: float, x2: float, y2: float,
            geometry: GeometryConfig
    ) -> tuple[float, float, float]:
        """"""

        first_t = 1.0
        hit_point = (x2, y2)

        for obstacle in geometry.obstacles:
            hit = GeometryFunctions._segment_rectangle_collision(
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                rect=obstacle,
            )

            if hit is None:
                continue

            t, hx, hy = hit

            if t < first_t:
                first_t = t
                hit_point = (hx, hy)

        x2, y2 = hit_point
        x2 = MathFunctions.clip(x2, geometry.borders.min_x, geometry.borders.max_x)
        y2 = MathFunctions.clip(y2, geometry.borders.min_y, geometry.borders.max_y)

        return x2, y2, first_t

    @staticmethod
    def _segment_rectangle_collision(
            x1: float,
            y1: float,
            x2: float,
            y2: float,
            rect: RectangleObstacle,
            eps: float = 1e-3,
    ) -> tuple[float, float, float] | None:
        """"""

        rx_min = rect.x_left_down
        rx_max = rect.x_right_up
        ry_min = rect.y_left_down
        ry_max = rect.y_right_up

        dx = x2 - x1
        dy = y2 - y1

        # Если старт уже строго внутри препятствия
        if (
                rx_min + eps < x1 < rx_max - eps
                and ry_min + eps < y1 < ry_max - eps
        ):
            return 0.0, x1, y1

        t_min = 0.0
        t_max = 1.0

        # X slab
        if abs(dx) < eps:
            # Параллельно вертикальным сторонам.
            # Если x строго вне прямоугольника или ровно на стене — входа внутрь нет.
            if x1 <= rx_min + eps or x1 >= rx_max - eps:
                return None
        else:
            tx1 = (rx_min - x1) / dx
            tx2 = (rx_max - x1) / dx

            tx_enter = min(tx1, tx2)
            tx_exit = max(tx1, tx2)

            t_min = max(t_min, tx_enter)
            t_max = min(t_max, tx_exit)

        # Y slab
        if abs(dy) < eps:
            # Параллельно горизонтальным сторонам.
            # Если y строго вне прямоугольника или ровно на стене — входа внутрь нет.
            if y1 <= ry_min + eps or y1 >= ry_max - eps:
                return None
        else:
            ty1 = (ry_min - y1) / dy
            ty2 = (ry_max - y1) / dy

            ty_enter = min(ty1, ty2)
            ty_exit = max(ty1, ty2)

            t_min = max(t_min, ty_enter)
            t_max = min(t_max, ty_exit)

        if t_min > t_max + eps:
            return None

        if t_min < -eps or t_min > 1.0 + eps:
            return None

        hit_x = x1 + dx * t_min
        hit_y = y1 + dy * t_min

        # Касание границы не считаем коллизией.
        probe_t = min(1.0, t_min + eps * 10)
        probe_x = x1 + dx * probe_t
        probe_y = y1 + dy * probe_t

        enters_inside = (
                rx_min + eps < probe_x < rx_max - eps
                and ry_min + eps < probe_y < ry_max - eps
        )

        if not enters_inside:
            return None

        return max(0.0, t_min), hit_x, hit_y

    @staticmethod
    def _quant_value(value, v_min, v_max, quants) -> int:
        """"""

        value = MathFunctions.clip(value, v_min, v_max)

        if quants <= 1:
            return 0

        if value == v_max:
            return quants - 1

        quant_size = v_max - v_min
        value = (value - v_min) / (quant_size / quants)
        return int(value)
