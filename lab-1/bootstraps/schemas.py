from abc import (
    ABC,
    abstractmethod,
)
from typing import Any

from framework.bootstraps.bootstrap import Bootstrap


class SchemaBootstrap(Bootstrap, ABC):

    @abstractmethod
    def awake(self) -> Any:
        """"""
        raise NotImplementedError("")
