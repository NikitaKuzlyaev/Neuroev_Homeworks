from bootstraps.environment_bootstrap import EnvironmentBootstrap
from bootstraps.geometry_bootstrap import GeometryBootstrap
from bootstraps.params_bootstrap import ParamsBootstrap
from bootstraps.rules_bootstrap import RulesBootstrap
from framework.app import App
from framework.context import Context

context = Context()
context.add_bootstrap(EnvironmentBootstrap())
context.add_bootstrap(RulesBootstrap())
context.add_bootstrap(GeometryBootstrap())
context.add_bootstrap(ParamsBootstrap())

app = App(context=context)
app.run()

print("Hello")


