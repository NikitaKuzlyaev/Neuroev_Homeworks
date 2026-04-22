from agents.agent import Agent
from gyms.gym import Gym
from politics.politic import Politic


class MyGym(Gym):

    def __init__(self, agent: Agent, politic: Politic):
        self.agent = agent
        self.politic = politic

    def step(self):
        print("step")

    def reset(self):
        ...
