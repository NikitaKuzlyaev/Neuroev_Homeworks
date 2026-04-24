from agents.agent import Agent
from bootstraps.key_registry import StorageKey
from framework.context import Context
from gyms.common.agent_spawner import AgentSpawner
from gyms.gym import Gym
from politics.states.state import State


class MyGym(Gym):

    def __init__(self, context: Context, agent: Agent):
        self.context = context
        self.agent = agent
        self.reset()

    def step(self):
        self.agent.step()
        print("step")

    def reset(self):
        x, y = AgentSpawner.get_spawn_point(self.context.get(StorageKey.GEO.value))
        print(x, y)
        state = State(x=x, y=y, b=0.0, v=0.0)
        self.agent.state = state
