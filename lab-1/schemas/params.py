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


class Field(BaseModel):
    x: int
    y: int
    b: int
    v: int


class DirectionOption(BaseModel):
    type: Literal["direction-option"]
    id: str
    radians: float


class Battery(BaseModel):
    speed_coef: float
    wind_x_coef: float
    wind_y_coef: float


class Quants(BaseModel):
    field: Field


class Agent(BaseModel):
    speed: List[SpeedOption]
    direction: List[DirectionOption]
    influence: Influence
    battery: Battery
    quants: Quants


class Config(BaseModel):
    agent: Agent
