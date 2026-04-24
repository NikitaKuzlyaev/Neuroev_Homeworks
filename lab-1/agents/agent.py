from abc import ABC, abstractmethod

from politics.states.state import State
from schemas.action import Action


class Agent(ABC):

    def __init__(self, state: State):
        self.state = state
        ...

    @abstractmethod
    def step(self):
        raise NotImplementedError("")

    @abstractmethod
    def reset(self):
        raise NotImplementedError("")

    @abstractmethod
    def propagate(self, old_state: State, new_state: State, action: Action, reward: float, done: bool = False):
        raise NotImplementedError("")
