import math

from bootstraps.key_registry import StorageKey
from evaluation.datacollectors.datacollector import PointCollector
from evaluation.plotters.position_heatmap import plot_heatmap
from framework.app import App
from gyms.gym import Gym, TerminalCondition

collector = PointCollector()


class Pipeline:

    def __init__(self, app: App, gym: Gym):
        self.app = app
        self.gym = gym

    def run(self):
        epoch_n = 1
        while True:
            self.gym.reset()

            condition: TerminalCondition = self.epoch()
            if condition == TerminalCondition.SUCCESS:
                ...
                #print("YAAAAA!!!!")
                #break

            print(f"end epoch {epoch_n}")
            epoch_n += 1

            if epoch_n % 1000 == 0:
                plot_heatmap(
                    points=collector.points,
                    x_min=0,
                    x_max=26,
                    y_min=0,
                    y_max=14,
                    bins_x=52,
                    bins_y=28,
                )
                collector.clear()

    def epoch(self) -> TerminalCondition:
        time_on_charge_area = 0

        while True:
            condition: TerminalCondition = self.gym.step()
            _geometry = self.app.context.get(StorageKey.GEO.value)
            I = math.dist(
                (self.gym.agent.state.x, self.gym.agent.state.y),
                (_geometry.target.x, _geometry.target.y)
            ) < _geometry.target.r
            if I:
                time_on_charge_area += 1

            if condition != TerminalCondition.NOTHING:
                # print(self.gym.agent.state.x, self.gym.agent.state.y)
                self.gym.reset()
                break

        #print(time_on_charge_area)
        return condition
