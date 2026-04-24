from agents.rational_ql import RationalQleaningAgent
from bootstraps.action_bootstrap import ActionBootstrap
from bootstraps.environment_bootstrap import EnvironmentBootstrap
from bootstraps.geometry_bootstrap import GeometryBootstrap
from bootstraps.key_registry import StorageKey
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
context.add_bootstrap(ActionBootstrap())

app = App(context=context)
app.run()

politic = EGreedyPolitic(epsilon=1.0, epsilon_min=0.1, fading=0.999)
state = State(0, 0, 0, 0)

params: ParamsConfig = context.get(StorageKey.PARAMS.value)
table = Table(
    n_states=params.agent.quants.x * params.agent.quants.y * params.agent.quants.b * params.agent.quants.v,
    n_actions=len(context.get(StorageKey.ACTION.value).actions)
)

agent = RationalQleaningAgent(state=state, context=context, politic=politic, table=table, alpha=1.0, gamma=0.99)

gym = MyGym(context=context, agent=agent)

pipeline = Pipeline(app=app, gym=gym)
pipeline.run()

print("Hello")
