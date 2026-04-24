from abc import ABC, abstractmethod
from enum import Enum

from agents.agent import Agent
from framework.context import Context
from politics.states.state import State


class TerminalCondition(Enum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    NOTHING = "NOTHING"


class Gym(ABC):

    def __init__(self, context: Context, agent: Agent):
        self.context = context
        self.agent = agent

    @abstractmethod
    def step(self) -> TerminalCondition:
        raise NotImplementedError("")

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError("")

    @abstractmethod
    def check_terminal(self, state: State) -> bool:
        raise NotImplementedError
