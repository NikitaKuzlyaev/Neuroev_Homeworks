from agents.agent import Agent
from politics.politic import Politic
from politics.states.state import State
from politics.table import Table


class RationalQleaningAgent(Agent):

    def __init__(self, state: State, politic: Politic, table: Table):
        self.state = state
        self.politic = politic
        self.table = table

    def step(self):
        pass

    def propagate(self):
        pass
