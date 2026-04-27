from bootstraps.key_registry import StorageKey
from bootstraps.schemas import SchemaBootstrap
from framework.bootstraps.decs.bootstrap_resource import bootstrap_resource
from framework.bootstraps.decs.context_storage import context_storage
from schemas.geometry import GeometryConfig
from utils.yaml_reader import YAMLReader


@bootstrap_resource("configurations/geometry.yaml")
class GeometryBootstrap(SchemaBootstrap):

    @context_storage(StorageKey.GEO.value)
    def awake(self) -> GeometryConfig:
        """"""
        data = YAMLReader.yaml_2_map(path=self.__class__.resource_path)
        return GeometryConfig(**data)
