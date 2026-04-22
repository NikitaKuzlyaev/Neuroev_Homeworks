from typing import (
    List,
    Literal,
)

from pydantic import BaseModel


class SpeedOption(BaseModel):
    type: Literal["speed-option"]
    id: str
    value: float


class Influence(BaseModel):
    wind_x_coef: float
    wind_y_coef: float


class Battery(BaseModel):
    speed_coef: float
    wind_x_coef: float
    wind_y_coef: float


class Agent(BaseModel):
    speed: List[SpeedOption]
    influence: Influence
    battery: Battery


class Config(BaseModel):
    agent: Agent
