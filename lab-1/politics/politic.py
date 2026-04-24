from abc import ABC, abstractmethod

from politics.table import Table


class Politic(ABC):

    @abstractmethod
    def make_action(self, table: Table, state_idx: int, n_actions: int):
        raise NotImplementedError("")
