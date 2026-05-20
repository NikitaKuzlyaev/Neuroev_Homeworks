import math
import os

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

winrate_counter = LastNWinrateCounter(n=250)
winrates = []

cdf_epoch_time_counter = CDFCounter(n=250)
epoch_times = []


class TrainingPipeline(Runnable):

    def __init__(self, app: App, gym: Gym):
        """"""
        self.app = app
        self.gym = gym
        self._geometry = self.app.context.get(StorageKey.GEO.value)

        # metric storage for periodic stats
        self._metric_successes: list[int] = []
        self._metric_times: list[int] = []
        self._metric_energies: list[float] = []
        self._metric_collisions: list[int] = []
        # ensure stats directory


    def run(self) -> None:
        """"""
        epoches = 50000

        for epoch_n in range(1, epoches + 1):
            """"""
            # === start of epoch

            self.gym.reset()
            tr: TerminalResult = self.epoch()

            # collect metrics and run analysis
            self.__analysis_pipeline(
                epoch_n=epoch_n,
                condition=tr.condition,
                episode_time=tr.metrics['episode_time'],
                energy_consumed=tr.metrics.get('energy_consumed', 0.0),
                collisions=tr.metrics.get('collisions', 0),
            )

            if epoch_n % 250 == 0:
                print(f"end epoch {epoch_n} winrate {winrate_counter.winrate()}")

            # === end of epoch
            #

            if epoch_n % 1000 == 0:
                save_list_to_json(data=self.gym.agent.table.q, file_path=f"misc/tables/agent3/qq_table_{epoch_n}")

                self._plot_winrate(winrates=winrates, save_path=f"misc/winrate/agent3/{epoch_n}.png")
                cdf_x, cdf_y = cdf_epoch_time_counter.get()
                self._plot_cdf_epoch_time(x=cdf_x, y=cdf_y, save_path=f"misc/cdf/agent3/{epoch_n}.png")

    def epoch(self) -> TerminalResult:
        """"""
        episode_time = 0
        time_on_charge_area = 0
        collisions_count = 0
        start_battery = self.gym.agent.state.b

        while True:
            tr: TerminalResult = self.gym.step(validate=False, tick=episode_time)
            episode_time += 1
            collisions_count += tr.metrics.get('collisions', 0)

            I = math.dist(
                (self.gym.agent.state.x, self.gym.agent.state.y),
                (self._geometry.target.x, self._geometry.target.y)
            ) < self._geometry.target.r

            if I:
                time_on_charge_area += 1

            if tr.condition != TerminalCondition.NOTHING:
                break

        final_battery = self.gym.agent.state.b
        energy_consumed = max(0.0, start_battery - final_battery)

        tr = TerminalResult(condition=tr.condition, metrics={
            "episode_time": episode_time,
            "collisions": collisions_count,
            "energy_consumed": energy_consumed,
        })

        return tr

    def _plot_heatmap(self, epoch: int) -> None:
        """"""
        plot_heatmap(
            points=collector.points,
            x_min=0, x_max=26, y_min=0, y_max=14,
            bins_x=104, bins_y=56,
            save_path=f"misc/heatmap/agent3/heatmap_epoch_{epoch:06d}.png",
            title=f"Heatmap посещенных точек, epoch={epoch}",
            vmin=0,
            vmax=200,
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
            self, epoch_n: int, condition: TerminalCondition, episode_time: int,
            energy_consumed: float = 0.0, collisions: int = 0,
    ) -> None:
        """"""
        # basic winrate tracking
        winrate_counter.update(condition=condition)
        winrates.append(winrate_counter.winrate())

        cdf_epoch_time_counter.update(episode_time)

        # append per-epoch detailed metrics
        self._metric_successes.append(1 if condition == TerminalCondition.SUCCESS else 0)
        self._metric_times.append(episode_time)
        self._metric_energies.append(energy_consumed)
        self._metric_collisions.append(collisions)

        # compute and write stats every 1000 epochs
        if epoch_n % 1000 == 0:
            window_size = 1000
            s_window = self._metric_successes[-window_size:]
            t_window = self._metric_times[-window_size:]
            e_window = self._metric_energies[-window_size:]
            c_window = self._metric_collisions[-window_size:]

            if len(s_window) == 0:
                return

            success_rate = sum(s_window) / len(s_window) * 100.0
            avg_time = sum(t_window) / len(t_window)
            avg_energy = sum(e_window) / len(e_window)
            collisions_percent = sum(c_window) / sum(t_window) * 100.0

            stats_path = os.path.join("misc", "stats", "agent3", f"stats_epoch_{epoch_n}.txt")
            with open(stats_path, "w", encoding="utf-8") as fh:
                fh.write("Метрики:\n")
                fh.write(f"успех(%): {success_rate:.2f}\n")
                fh.write(f"время до успеха: {avg_time:.2f}\n")
                fh.write(f"расход энергии: {avg_energy:.6f}\n")
                fh.write(f"коллизии(%): {collisions_percent:.2f}\n")

        if epoch_n % 1000 == 0:  # todo:  disable
            self._plot_heatmap(epoch=epoch_n)
            collector.clear()
