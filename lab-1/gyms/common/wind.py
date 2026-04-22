from random import random

from framework.context import Context
from schemas.environment import EnvironmentConfig


class WindManager:

    def __init__(self, context: Context):
        self.context = context
        self.wx = 0
        self.wy = 0

        self.change_direction()

    def change_direction(self) -> None:
        env: EnvironmentConfig = self.context.get("env")

        wx = env.wind.direction.x.min + random() / (env.wind.direction.x.max - env.wind.direction.x.min)
        wy = env.wind.direction.y.min + random() / (env.wind.direction.y.max - env.wind.direction.y.min)

        self.wx = wx
        self.wy = wy
