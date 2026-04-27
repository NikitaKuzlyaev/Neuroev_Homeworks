import math

from bootstraps.key_registry import StorageKey
from evaluation.datacollectors.datacollector import PointCollector
from evaluation.plotters.position_heatmap import plot_heatmap
from framework.app import App
from gyms.gym import (
    Gym,
    TerminalCondition,
)
from utils.json_saving import save_list_to_json

collector = PointCollector()


class Pipeline:

    def __init__(self, app: App, gym: Gym):
        """"""
        self.app = app
        self.gym = gym
        self._geometry = self.app.context.get(StorageKey.GEO.value)

    def run(self) -> None:
        """"""
        epoches = 1000

        for epoch_n in range(1, epoches + 1):
            """"""
            # === start of epoch

            self.gym.reset()
            condition: TerminalCondition = self.epoch()
            print(f"end epoch {epoch_n}")

            # === end of epoch

            if epoch_n % 1000 == -1:  # todo: its disable
                self._plot_heatmap()
                collector.clear()

        save_list_to_json(data=self.gym.agent._table.q, file_path="q_table_15k")

    def epoch(self) -> TerminalCondition:
        """"""
        time_on_charge_area = 0

        while True:
            condition: TerminalCondition = self.gym.step()

            I = math.dist(
                (self.gym.agent.state.x, self.gym.agent.state.y),
                (self._geometry.target.x, self._geometry.target.y)
            ) < self._geometry.target.r

            if I:
                time_on_charge_area += 1

            if condition != TerminalCondition.NOTHING:
                self.gym.reset()
                break

        return condition

    def _plot_heatmap(self) -> None:
        """"""
        plot_heatmap(
            points=collector.points,
            x_min=0, x_max=26, y_min=0, y_max=14,
            bins_x=52, bins_y=28,
        )
