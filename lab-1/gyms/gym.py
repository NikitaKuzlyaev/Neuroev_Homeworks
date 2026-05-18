from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from agents.agent import Agent
from framework.context import Context
from politics.states.state import State


class TerminalCondition(Enum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    NOTHING = "NOTHING"


@dataclass
class TerminalResult:
    condition: TerminalCondition
    metrics: dict[str, Any] = field(default_factory=dict)


class Gym(ABC):

    def __init__(self, context: Context, agent: Agent):
        """"""
        self.context = context
        self.agent = agent

    @abstractmethod
    def step(self, validate: bool = False, tick: int = 0) -> TerminalResult:
        """"""
        raise NotImplementedError("")

    @abstractmethod
    def reset(self) -> None:
        """"""
        raise NotImplementedError("")

    @abstractmethod
    def check_terminal(self, state: State) -> bool:
        """"""
        raise NotImplementedError
