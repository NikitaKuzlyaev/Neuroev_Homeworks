from typing import (
    List,
    Literal,
)

from pydantic import BaseModel


class SpeedOption(BaseModel):
    type: Literal["speed-option"]
    id: str
    value: float


class Speed(BaseModel):
    min_value: float
    max_value: float
    options: List[SpeedOption]


class Influence(BaseModel):
    wind_x_coef: float
    wind_y_coef: float


class Quants(BaseModel):
    x: int
    y: int
    b: int
    v: int


class DirectionOption(BaseModel):
    type: Literal["direction-option"]
    id: str
    radians: float


class Battery(BaseModel):
    min_value: float
    max_value: float
    speed_coef: float
    wind_x_coef: float
    wind_y_coef: float


class Agent(BaseModel):
    speed: Speed
    direction: List[DirectionOption]
    influence: Influence
    battery: Battery
    quants: Quants


class ParamsConfig(BaseModel):
    agent: Agent
