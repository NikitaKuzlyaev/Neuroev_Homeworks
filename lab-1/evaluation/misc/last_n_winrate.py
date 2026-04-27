from collections import deque

from gyms.gym import TerminalCondition


class LastNWinrateCounter:

    def __init__(self, n=250):
        """"""
        self._n = n
        self._last = deque()
        self._wins = 0

    def update(self, condition: TerminalCondition) -> None:
        """"""

        if condition == TerminalCondition.SUCCESS:
            self._last.append(1)
            self._wins += 1
        else:
            self._last.append(0)

        while len(self._last) > self._n:
            f = self._last.popleft()
            self._wins -= f

    def winrate(self) -> float:
        """"""
        wr = self._wins / self._n
        return wr
