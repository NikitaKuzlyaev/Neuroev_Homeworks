from abc import ABC, abstractmethod


class Bootstrap(ABC):

    @abstractmethod
    def awake(self):
        raise NotImplementedError("method not implemented")
