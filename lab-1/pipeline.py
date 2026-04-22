import time

from framework.app import App
from gyms.gym import Gym


class Pipeline:

    def __init__(self, app: App, gym: Gym):
        self.app = app
        self.gym = gym

    def run(self):

        for _ in range(10):
            self.gym.reset()

            res = self.epoch()


    def epoch(self) -> bool:

        for _ in range(100):
            self.gym.step()
            time.sleep(1)

        return True
