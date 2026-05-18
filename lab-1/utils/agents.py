from agents.agent import Agent
from agents.prospect_theory_agent import ProspectTheoryQleaningAgent
from agents.rational_ql import RationalQleaningAgent
from agents.risk_sensitive import RiskSensitiveQleaningAgent
from framework.context import Context
from politics.e_greedy import EGreedyPolitic
from politics.states.state import State
from politics.table import Table


def create_ql_greedy(
        state: State, context: Context, table: Table, start_epoch=1
) -> Agent:
    """"""
    politic = EGreedyPolitic(
        epsilon=1.0,
        epsilon_min=0.01,
        fading=0.997,
    )
    for i in range(start_epoch - 1):
        politic.degradation()

    agent = RationalQleaningAgent(
        state=state,
        context=context,
        politic=politic,
        table=table,
        alpha=1.0,
        gamma=0.99,
    )
    return agent


def create_ql_prospect(
        state: State, context: Context, table: Table, start_epoch=1
) -> Agent:
    """"""
    politic = EGreedyPolitic(
        epsilon=1.0,
        epsilon_min=0.01,
        fading=0.997,
    )
    for i in range(start_epoch - 1):
        politic.degradation()

    agent = ProspectTheoryQleaningAgent(
        state=state,
        context=context,
        politic=politic,
        table=table,
        gamma=0.99,
    )
    return agent


def create_risk_sensitive(
        state: State, context: Context, table: Table, start_epoch=1
) -> Agent:
    """"""
    politic = EGreedyPolitic(
        epsilon=1.0,
        epsilon_min=0.01,
        fading=0.997,
    )
    for i in range(start_epoch - 1):
        politic.degradation()

    agent = RiskSensitiveQleaningAgent(
        state=state,
        context=context,
        politic=politic,
        table=table,
        gamma=0.99,
    )
    return agent
