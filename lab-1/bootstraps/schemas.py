from abc import ABC, abstractmethod

from framework.bootstraps.bootstrap import Bootstrap


# from framework.bootstraps.registry import BootstrapRegistry


# @BootstrapRegistry.register_bootstrap
class SchemaBootstrap(Bootstrap, ABC):

    @abstractmethod
    def awake(self):
        ...
