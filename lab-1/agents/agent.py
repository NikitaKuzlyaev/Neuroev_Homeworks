from abc import ABC, abstractmethod

from politics.politic import Politic
from politics.states.state import State
from politics.table import Table


class Agent(ABC):

    def __init__(self, state: State, politic: Politic, table: Table):
        self.state = state
        self.politic = politic
        self.table = table

    @abstractmethod
    def step(self):
        raise NotImplementedError("")

    @abstractmethod
    def propagate(self):
        raise NotImplementedError("")
