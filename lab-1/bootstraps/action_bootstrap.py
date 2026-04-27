from bootstraps.key_registry import StorageKey
from bootstraps.schemas import SchemaBootstrap
from framework.bootstraps.decs.bootstrap_resource import bootstrap_resource
from framework.bootstraps.decs.context_storage import context_storage
from schemas.action import (
    Action,
    Actions,
)
from schemas.params import (
    SpeedOption,
    DirectionOption,
)
from utils.yaml_reader import YAMLReader


@bootstrap_resource("configurations/params.yaml")
class ActionBootstrap(SchemaBootstrap):

    @context_storage(StorageKey.ACTION.value)
    def awake(self) -> Actions:
        """"""
        data = YAMLReader.yaml_2_map(path=self.__class__.resource_path)

        speed_list = data["agent"]["speed"]["options"]  # фуу блин
        direction_list = data["agent"]["direction"]
        actions_list = []

        for speed_op in speed_list:
            speed = SpeedOption(**speed_op)

            for direction_op in direction_list:
                direction = DirectionOption(**direction_op)

                action = Action(speed=speed, direction=direction)
                actions_list.append(action)

        actions_model = Actions(**{"actions": actions_list})
        return actions_model
