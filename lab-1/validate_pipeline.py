import math

from bootstraps.key_registry import StorageKey
from evaluation.datacollectors.datacollector import PointCollector
from evaluation.misc.last_n_winrate import LastNWinrateCounter
from framework.app import App
from gyms.gym import (
    Gym,
    TerminalCondition, TerminalResult,
)
from mixins.runnable import Runnable

collector = PointCollector()
winrate_counter = LastNWinrateCounter(n=300)
winrates = []


class ValidatePipeline(Runnable):

    def __init__(self, app: App, gym: Gym):
        """"""
        self.app = app
        self.gym = gym
        self._geometry = self.app.context.get(StorageKey.GEO.value)

    def run(self) -> None:
        """"""
        epoches = 300

        collisions_total = 0
        episode_time_total = 0

        for epoch_n in range(1, epoches + 1):
            """"""
            # === start of epoch

            self.gym.reset()
            tr: TerminalResult = self.epoch()

            self.__analysis_pipeline(epoch_n=epoch_n, condition=tr.condition)
            collisions_total += tr.metrics["collisions"]
            episode_time_total += tr.metrics["episode_time"]

            # === end of epoch

        print(f"winrate: {winrate_counter.winrate()}")
        print(f"collisions_p: {collisions_total / episode_time_total}")
        print(f"episode_time_avg: {episode_time_total / epoches}")

    def epoch(self) -> TerminalResult:
        """"""
        episode_time = 0
        collisions_count = 0

        while True:
            tr: TerminalResult = self.gym.step(validate=True, tick=episode_time)
            collisions_count += tr.metrics["collisions"]
            episode_time += 1

            I = math.dist(
                (self.gym.agent.state.x, self.gym.agent.state.y),
                (self._geometry.target.x, self._geometry.target.y)
            ) < self._geometry.target.r

            if I:
                # time_on_charge_area += 1
                ...

            if tr.condition != TerminalCondition.NOTHING:
                self.gym.reset()
                break

        return TerminalResult(
            condition=tr.condition,
            metrics={
                "collisions": collisions_count,
                "episode_time": episode_time - 1,
            }
        )

    def __analysis_pipeline(self, epoch_n: int, condition: TerminalCondition):
        """"""
        winrate_counter.update(condition=condition)
        winrates.append(winrate_counter.winrate())
