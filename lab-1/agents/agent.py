from abc import (
    ABC,
    abstractmethod,
)

from framework.context import Context
from politics.politic import Politic
from politics.states.state import State
from politics.table import Table
from schemas.action import Action
from schemas.agent import StepResponse


class Agent(ABC):

    def __init__(self, state: State, context: Context, politic: Politic, table: Table):
        """"""
        self.state = state
        self._context = context
        self._politic = politic
        self._table = table

    @abstractmethod
    def step(self) -> StepResponse:
        """"""
        raise NotImplementedError("")

    @abstractmethod
    def reset(self) -> None:
        """"""
        raise NotImplementedError("")

    @abstractmethod
    def propagate(self, old_state: State, new_state: State, action: Action, reward: float, done: bool = False) -> None:
        """"""
        raise NotImplementedError("")
