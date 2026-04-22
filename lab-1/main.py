from agents.rational_ql import RationalQleaningAgent
from bootstraps.environment_bootstrap import EnvironmentBootstrap
from bootstraps.geometry_bootstrap import GeometryBootstrap
from bootstraps.params_bootstrap import ParamsBootstrap
from bootstraps.rules_bootstrap import RulesBootstrap
from framework.app import App
from framework.context import Context
from gyms.my_gym import MyGym
from pipeline import Pipeline
from politics.e_greedy import EGreedyPolitic
from politics.states.state import State
from politics.table import Table
from schemas.params import ParamsConfig

context = Context()
context.add_bootstrap(EnvironmentBootstrap())
context.add_bootstrap(RulesBootstrap())
context.add_bootstrap(GeometryBootstrap())
context.add_bootstrap(ParamsBootstrap())

app = App(context=context)
app.run()

politic = EGreedyPolitic()
state = State(0, 0, 0, 0)

params: ParamsConfig = context.get("params")
table = Table(size=params.agent.quants.x * params.agent.quants.y * params.agent.quants.b * params.agent.quants.v)
agent = RationalQleaningAgent(state=state, politic=politic, table=table)

gym = MyGym(context=context, agent=agent)

pipeline = Pipeline(app=app, gym=gym)
pipeline.run()

print("Hello")
