from pydantic import BaseModel


class Range(BaseModel):
    min: float
    max: float


class Direction(BaseModel):
    x: Range
    y: Range


class Update(BaseModel):
    rate: int


class Wind(BaseModel):
    type: str
    direction: Direction
    update: Update


class EnvironmentConfig(BaseModel):
    wind: Wind


