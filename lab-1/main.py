from bootstraps.action_bootstrap import ActionBootstrap
from bootstraps.environment_bootstrap import EnvironmentBootstrap
from bootstraps.geometry_bootstrap import GeometryBootstrap
from bootstraps.key_registry import StorageKey
from bootstraps.params_bootstrap import ParamsBootstrap
from bootstraps.rules_bootstrap import RulesBootstrap
from framework.app import App
from framework.context import Context
from gyms.my_gym import MyGym
from politics.states.state import State
from politics.table import Table
from schemas.params import ParamsConfig
from training_pipeline import TrainingPipeline
from utils.agents import create_ql_prospect, create_ql_greedy
from utils.json_saving import load_list_from_json
from validate_pipeline import ValidatePipeline

context = Context()
context.add_bootstrap(EnvironmentBootstrap())
context.add_bootstrap(RulesBootstrap())
context.add_bootstrap(GeometryBootstrap())
context.add_bootstrap(ParamsBootstrap())
context.add_bootstrap(ActionBootstrap())

app = App(context=context)
app.run()

state = State(x=0, y=0, b=0, v=0)

params: ParamsConfig = context.get(StorageKey.PARAMS.value)

table = Table(
    n_states=params.agent.quants.x * params.agent.quants.y * params.agent.quants.b * params.agent.quants.v,
    n_actions=len(context.get(StorageKey.ACTION.value).actions)
)

# ======================  TRAIN  ========================================


agent1 = create_ql_greedy(state=state, context=context, table=table)
# agent2 = create_ql_prospect(state=state, context=context, table=table)
# agent3 = create_risk_sensitive(state=state, context=context, table=table)

gym = MyGym(
    context=context,
    agent=agent1,
)

training = TrainingPipeline(app=app, gym=gym)
training.run()


# ======================  VALIDATE  ========================================

# start_epoch = 15000
#table.q = load_list_from_json(file_path="misc/tables/agent2/qq_table_45000")
# # agent1 = create_ql_greedy(state=state, context=context, table=table, start_epoch=start_epoch)
# agent2 = create_ql_prospect(state=state, context=context, table=table)
# # agent3 = create_risk_sensitive(state=state, context=context, table=table)
#
# gym = MyGym(
#     context=context,
#     agent=agent2,
# )
#
# validate = ValidatePipeline(app=app, gym=gym)
# validate.run()

print("Hello")
