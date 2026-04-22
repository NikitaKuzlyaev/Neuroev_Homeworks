from bootstraps.schemas import SchemaBootstrap
from framework.bootstraps.decs.bootstrap_resource import bootstrap_resource
from framework.bootstraps.decs.context_storage import context_storage
from schemas.environment import EnvironmentConfig
from utils.yaml_reader import YAMLReader


@bootstrap_resource("configurations/environment.yaml")
class EnvironmentBootstrap(SchemaBootstrap):

    @context_storage("env")
    def awake(self):
        data = YAMLReader.yaml_2_map(path=self.__class__.resource_path)
        return EnvironmentConfig(**data)

