from typing import (
    List,
    Literal,
)

from pydantic import BaseModel


class Borders(BaseModel):
    min_x: float
    max_x: float
    min_y: float
    max_y: float


class SpawnClip(BaseModel):
    min_x: float
    max_x: float
    min_y: float
    max_y: float


class Spawn(BaseModel):
    clip: SpawnClip
    mean_x: float
    mean_y: float
    std: float


class Target(BaseModel):
    x: float
    y: float
    r: float


class RectangleObstacle(BaseModel):
    type: Literal["rectangle"]
    id: str
    x_left_down: float
    y_left_down: float
    x_right_up: float
    y_right_up: float


class Config(BaseModel):
    borders: Borders
    spawn: Spawn
    target: Target
    obstacles: List[RectangleObstacle]
