import math
from random import random

from schemas.geometry import GeometryConfig
from utils.math_funcs import MathFunctions


class AgentSpawner:

    @staticmethod
    def get_spawn_point(geometry: GeometryConfig) -> tuple[float, float]:
        u = random()
        v = random()

        r = geometry.spawn.r * math.sqrt(u)
        theta = 2 * math.pi * v

        x = geometry.spawn.mean_x + r * math.cos(theta)
        y = geometry.spawn.mean_y + r * math.sin(theta)

        # clipping
        x_left, x_right = geometry.spawn.clip.min_x, geometry.spawn.clip.max_x
        y_left, y_right = geometry.spawn.clip.min_y, geometry.spawn.clip.max_y

        x = MathFunctions.clip(x, x_left, x_right)
        y = MathFunctions.clip(y, y_left, y_right)

        return x, y
