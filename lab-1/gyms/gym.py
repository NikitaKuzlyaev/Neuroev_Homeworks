from abc import ABC, abstractmethod


class Gym(ABC):

    @abstractmethod
    def step(self):
        raise NotImplementedError("")

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError("")

    @abstractmethod
    def check_terminal(self) -> bool:
        raise NotImplementedError
