from abc import (
    ABC,
    abstractmethod,
)
from typing import Any


class Container(ABC):

    @abstractmethod
    def set_metrics(self, data: dict[Any, Any]) -> None:
        """"""
        raise NotImplementedError("")

    @abstractmethod
    def get_metrics(self) -> dict[Any, Any]:
        """"""
        raise NotImplementedError("")
