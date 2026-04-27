import random

from mixins.degradational import Degradational
from politics.politic import Politic
from politics.table import Table
from utils.math_funcs import MathFunctions


class EGreedyPolitic(Politic, Degradational):

    def __init__(self, epsilon: float = 1.0, epsilon_min: float = 0.01, fading: float = 0.997):
        """"""
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.fading = fading

    def make_action(self, table: Table, state_idx: int, n_actions: int) -> int:
        """"""
        if random.random() < self.epsilon:
            return random.randrange(n_actions)

        return table.best_action(state_idx)

    def degradation(self) -> None:
        """"""
        new_epsilon = MathFunctions.clip_left(self.epsilon * self.fading, self.epsilon_min)
        self.epsilon = new_epsilon
