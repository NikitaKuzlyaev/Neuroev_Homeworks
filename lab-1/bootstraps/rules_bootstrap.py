from bootstraps.schemas import SchemaBootstrap
from framework.bootstraps.decs.bootstrap_resource import bootstrap_resource
from framework.bootstraps.decs.context_storage import context_storage
from schemas.rules import RulesConfig
from utils.yaml_reader import YAMLReader


@bootstrap_resource("configurations/rules.yaml")
class RulesBootstrap(SchemaBootstrap):

    @context_storage("rules")
    def awake(self):
        data = YAMLReader.yaml_2_map(path=self.__class__.resource_path)
        return RulesConfig(**data)

