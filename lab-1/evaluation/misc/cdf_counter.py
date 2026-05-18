from collections import deque


class CDFCounter:

    def __init__(self, n: int = 150, max_time: int = 210):
        """"""
        self._n = n
        self._max_time = max_time
        self._last = deque()

    def update(self, time: int) -> None:
        """"""
        self._last.append(time)

        while len(self._last) > self._n:
            self._last.popleft()

    def get_x(self) -> list[int]:
        """"""
        return list(range(self._max_time + 1))

    def get_y(self) -> list[float]:
        """"""
        if len(self._last) == 0:
            return [0.0 for _ in range(self._max_time + 1)]

        values = list(self._last)
        window_size = len(values)

        cdf = []

        for threshold_time in range(self._max_time + 1):
            count = 0

            for episode_time in values:
                if episode_time <= threshold_time:
                    count += 1

            cdf.append(count / window_size)

        return cdf

    def get(self) -> tuple[list[int], list[float]]:
        """"""
        return self.get_x(), self.get_y()
