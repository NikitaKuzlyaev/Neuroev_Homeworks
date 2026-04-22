import time

from framework.app import App
from gyms.gym import Gym


class Pipeline:

    def __init__(self, app: App, gym: Gym):
        self.app = app
        self.gym = gym

    def run(self):

        while True:
            self.epoch()


    def epoch(self):

        while True:
            self.gym.step()
            time.sleep(1)
