from random import random

from bootstraps.key_registry import StorageKey
from framework.context import Context
from schemas.environment import EnvironmentConfig
from schemas.params import ParamsConfig


class WindManager:

    def __init__(self, context: Context, rate: int = 25):
        self.context = context
        self.wx = 0
        self.wy = 0
        self._rate = rate
        self.__to_change_direction = rate

        self.env: EnvironmentConfig = self.context.get(StorageKey.ENV.value)
        self.params: ParamsConfig = self.context.get(StorageKey.PARAMS.value)

        self.__change_direction()

    def __change_direction(self) -> None:
        wx = self.env.wind.direction.x.min + random() * (self.env.wind.direction.x.max - self.env.wind.direction.x.min)
        wy = self.env.wind.direction.y.min + random() * (self.env.wind.direction.y.max - self.env.wind.direction.y.min)

        self.wx = wx * self.params.agent.influence.wind_x_coef
        self.wy = wy * self.params.agent.influence.wind_y_coef

    def update(self):
        self.__to_change_direction -= 1

        if self.__to_change_direction == 0:
            self.__to_change_direction = self._rate
            self.__change_direction()

    def reset(self):
        self.__to_change_direction = self._rate
        self.__change_direction()
