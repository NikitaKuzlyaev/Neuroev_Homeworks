from functools import wraps
from typing import Any, Callable

from politics.states.state import State


def get_nested_attr(obj: Any, path: str) -> Any:
    for part in path.split("."):
        obj = getattr(obj, part)
    return obj


class PointCollector:
    def __init__(self):
        self.points: list[tuple[float, float]] = []

    def collect_state(self, state: State) -> None:
        self.points.append((state.x, state.y))

    def clear(self) -> None:
        self.points.clear()


def datacollector(path: str, callback: Callable[[Any], None]):
    def decorator(func):
        @wraps(func)
        def wrap(self, *args, **kwargs):
            result = func(self, *args, **kwargs)

            value = get_nested_attr(self, path)
            callback(value)

            return result

        return wrap

    return decorator
