from random import random

from bootstraps.key_registry import StorageKey
from framework.context import Context
from schemas.environment import EnvironmentConfig


class WindManager:

    def __init__(self, context: Context):
        self.context = context
        self.wx = 0
        self.wy = 0

        self.change_direction()

    def change_direction(self) -> None:
        env: EnvironmentConfig = self.context.get(StorageKey.ENV.value)

        wx = env.wind.direction.x.min + random() / (env.wind.direction.x.max - env.wind.direction.x.min)
        wy = env.wind.direction.y.min + random() / (env.wind.direction.y.max - env.wind.direction.y.min)

        self.wx = wx
        self.wy = wy
