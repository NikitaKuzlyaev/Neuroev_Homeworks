from typing import List

from pydantic import BaseModel

from schemas.params import (
    SpeedOption,
    DirectionOption,
)


class Action(BaseModel):
    speed: SpeedOption
    direction: DirectionOption


class Actions(BaseModel):
    actions: List[Action]
