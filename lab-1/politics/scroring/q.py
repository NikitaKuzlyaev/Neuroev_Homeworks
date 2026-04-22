from abc import ABC

from politics.actions.action import Action
from politics.states.state import State


class Q(ABC):

    def score_action(self, state: State, action: Action) -> float:
        raise NotImplementedError("")
