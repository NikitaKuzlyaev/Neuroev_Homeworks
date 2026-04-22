from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class SuccessTerminal(BaseModel):
    max_abs_difference: float
    min_b: float
    max_t: int


class FailTerminal(BaseModel):
    max_b: float
    min_t: int


class Terminal(BaseModel):
    success: SuccessTerminal
    fail: FailTerminal


class ElseAward(BaseModel):
    base: float
    speed_coef: float
    I_station_coef: float


class Award(BaseModel):
    success: float
    fail: float
    else_: ElseAward = Field(alias="else")

    model_config = ConfigDict(populate_by_name=True)


class RulesBody(BaseModel):
    terminal: Terminal
    award: Award


class RulesConfig(BaseModel):
    rules: RulesBody

