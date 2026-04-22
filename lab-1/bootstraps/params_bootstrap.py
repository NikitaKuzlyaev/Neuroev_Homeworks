from bootstraps.schemas import SchemaBootstrap
from framework.bootstraps.decs.bootstrap_resource import bootstrap_resource
from framework.bootstraps.decs.context_storage import context_storage
from schemas.params import Config
from utils.yaml_reader import YAMLReader


@bootstrap_resource("configurations/params.yaml")
class ParamsBootstrap(SchemaBootstrap):

    @context_storage("params")
    def awake(self):
        data = YAMLReader.yaml_2_map(path=self.__class__.resource_path)
        return Config(**data)
