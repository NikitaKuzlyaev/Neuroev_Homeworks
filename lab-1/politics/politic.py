from abc import ABC, abstractmethod


class Politic(ABC):

    @abstractmethod
    def make_action(self):
        raise NotImplementedError("")
