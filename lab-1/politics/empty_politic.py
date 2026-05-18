from politics.politic import Politic
from politics.table import Table


class EmptyPolitic(Politic):

    def __init__(self):
        """"""

    def make_action(self, table: Table, state_idx: int, n_actions: int) -> int:
        """"""
        return table.best_action(state_idx)
