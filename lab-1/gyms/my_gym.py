from agents.agent import Agent
from framework.context import Context
from gyms.gym import Gym


class MyGym(Gym):

    def __init__(self, context: Context, agent: Agent):
        self.context = context
        self.agent = agent
        self.reset()

    def step(self):
        self.agent.step()
        print("step")

    def reset(self):
        self.agent.reset()
