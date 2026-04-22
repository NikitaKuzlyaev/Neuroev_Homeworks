from abc import ABC, abstractmethod


class Agent(ABC):

    @abstractmethod
    def step(self):
        raise NotImplementedError("")

    @abstractmethod
    def propagate(self):
        raise NotImplementedError("")
