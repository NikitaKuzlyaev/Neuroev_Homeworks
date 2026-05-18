import math

from bootstraps.key_registry import StorageKey
from evaluation.datacollectors.datacollector import PointCollector
from evaluation.misc.last_n_winrate import LastNWinrateCounter
from evaluation.plotters.plot_winrate import plot_winrate
from evaluation.plotters.position_heatmap import plot_heatmap
from framework.app import App
from gyms.gym import (
    Gym,
    TerminalCondition, TerminalResult,
)
from mixins.runnable import Runnable
from utils.json_saving import save_list_to_json

collector = PointCollector()
winrate_counter = LastNWinrateCounter(n=250)
winrates = []


class TrainingPipeline(Runnable):

    def __init__(self, app: App, gym: Gym):
        """"""
        self.app = app
        self.gym = gym
        self._geometry = self.app.context.get(StorageKey.GEO.value)

    def run(self) -> None:
        """"""
        epoches = 90000

        for epoch_n in range(1, epoches + 1):
            """"""
            # === start of epoch

            self.gym.reset()
            condition: TerminalCondition = self.epoch()

            self.__analysis_pipeline(epoch_n=epoch_n, condition=condition)

            if epoch_n % 50 == 0:
                print(f"end epoch {epoch_n} winrate {winrate_counter.winrate()}")

            if epoch_n % 15000 == 0:
                save_list_to_json(data=self.gym.agent.table.q, file_path=f"misc/tables/agent2/qq_table_{epoch_n}")
            # === end of epoch
        #
        # self._plot_winrate(winrates=winrates)
        save_list_to_json(data=self.gym.agent.table.q, file_path="misc/tables/qq_table_15k")

    def epoch(self) -> TerminalCondition:
        """"""
        episode_time = 0
        time_on_charge_area = 0

        while True:
            tr: TerminalResult = self.gym.step(validate=False, tick=episode_time)
            episode_time += 1

            I = math.dist(
                (self.gym.agent.state.x, self.gym.agent.state.y),
                (self._geometry.target.x, self._geometry.target.y)
            ) < self._geometry.target.r

            if I:
                time_on_charge_area += 1

            if tr.condition != TerminalCondition.NOTHING:
                self.gym.reset()
                break

        return tr.condition

    def _plot_heatmap(self, epoch: int) -> None:
        """"""
        plot_heatmap(
            points=collector.points,
            x_min=0, x_max=26, y_min=0, y_max=14,
            bins_x=52, bins_y=28,
            save_path=f"misc/frames/heatmap_epoch_{epoch:06d}.png",
            title=f"Heatmap посещенных точек, epoch={epoch}",
            vmin=0,
            vmax=500,
        )

    def _plot_winrate(self, winrates: list[float]) -> None:
        """"""
        plot_winrate(winrates=winrates, save_path="misc/winrate.png")

    def __analysis_pipeline(self, epoch_n: int, condition: TerminalCondition):
        """"""
        winrate_counter.update(condition=condition)
        winrates.append(winrate_counter.winrate())

        if epoch_n % 1000 == 0:  # todo: its disable
            self._plot_heatmap(epoch=epoch_n)
            collector.clear()
