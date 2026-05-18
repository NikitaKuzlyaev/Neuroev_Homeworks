import math

from bootstraps.key_registry import StorageKey
from evaluation.datacollectors.datacollector import PointCollector
from evaluation.misc.cdf_counter import CDFCounter
from evaluation.misc.last_n_winrate import LastNWinrateCounter
from evaluation.plotters.plot_winrate import plot_winrate, plot_success_time_cdf
from evaluation.plotters.position_heatmap import plot_heatmap
from framework.app import App
from gyms.gym import (
    Gym,
    TerminalCondition, TerminalResult,
)
from mixins.runnable import Runnable
from utils.json_saving import save_list_to_json

collector = PointCollector()

winrate_counter = LastNWinrateCounter(n=150)
winrates = []

cdf_epoch_time_counter = CDFCounter(n=150)
epoch_times = []


class TrainingPipeline(Runnable):

    def __init__(self, app: App, gym: Gym):
        """"""
        self.app = app
        self.gym = gym
        self._geometry = self.app.context.get(StorageKey.GEO.value)

    def run(self) -> None:
        """"""
        epoches = 40000

        for epoch_n in range(1, epoches + 1):
            """"""
            # === start of epoch

            self.gym.reset()
            tr: TerminalResult = self.epoch()

            self.__analysis_pipeline(epoch_n=epoch_n, condition=tr.condition, episode_time=tr.metrics['episode_time'])

            if epoch_n % 50 == 0:
                print(f"end epoch {epoch_n} winrate {winrate_counter.winrate()}")

            if epoch_n % 1000 == 0:
                save_list_to_json(data=self.gym.agent.table.q, file_path=f"misc/tables/agent1/qq_table_{epoch_n}")
                # === end of epoch
                #
                self._plot_winrate(winrates=winrates, save_path=f"misc/winrate/agent1/{epoch_n}.png")
                cdf_x, cdf_y = cdf_epoch_time_counter.get()
                self._plot_cdf_epoch_time(x=cdf_x, y=cdf_y, save_path=f"misc/cdf/agent1/{epoch_n}.png")

    def epoch(self) -> TerminalResult:
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
                break

        tr = TerminalResult(condition=tr.condition, metrics={"episode_time": episode_time})

        return tr

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

    def _plot_winrate(
            self, winrates: list[float], save_path: str
    ) -> None:
        """"""
        plot_winrate(winrates=winrates, save_path=save_path)

    def _plot_cdf_epoch_time(
            self, x: list[int], y: list[float], save_path: str
    ) -> None:
        """"""
        plot_success_time_cdf(x=x, y=y, save_path=save_path)

    def __analysis_pipeline(
            self, epoch_n: int, condition: TerminalCondition, episode_time: int
    ) -> None:
        """"""
        winrate_counter.update(condition=condition)
        winrates.append(winrate_counter.winrate())

        cdf_epoch_time_counter.update(episode_time)

        # if epoch_n % 1000 == 0:  # todo: its disable
        #     self._plot_heatmap(epoch=epoch_n)
        #     collector.clear()
