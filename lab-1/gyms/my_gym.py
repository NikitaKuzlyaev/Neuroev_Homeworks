import math

from agents.agent import Agent
from agents.common.geometry import GeometryFunctions
from agents.common.wind import WindManager
from bootstraps.key_registry import StorageKey
from framework.context import Context
from gyms.gym import Gym, TerminalCondition
from politics.states.state import State
from rules.movement import get_new_xy, get_new_b
from rules.reward import get_reward
from schemas.agent import StepResponse
from schemas.geometry import GeometryConfig
from schemas.params import ParamsConfig
from schemas.rules import RulesConfig


class MyGym(Gym):

    def __init__(self, context: Context, agent: Agent):
        super().__init__(context, agent)
        self.context = context
        self.agent = agent
        self._geometry: GeometryConfig = context.get(StorageKey.GEO.value)
        self._params: ParamsConfig = context.get(StorageKey.PARAMS.value)
        self._rules: RulesConfig = context.get(StorageKey.RULES.value)
        self._wind_manager: WindManager = WindManager(context=context)

        self.reset()

    def step(self) -> TerminalCondition:
        step: StepResponse = self.agent.step()

        state: State = self.agent.state
        xn, yn = get_new_xy(state=state, action=step.action, wind_manager=self._wind_manager)

        xe, ye = GeometryFunctions.get_next_position(x1=state.x, y1=state.y, x2=xn, y2=yn, geometry=self._geometry)

        # print("VV", math.dist((state.x, state.y), (xe, ye)))
        b = get_new_b(state=state, params=self._params, geometry=self._geometry, wind_manager=self._wind_manager)

        real_new_state = State(x=xe, y=ye, b=b, v=step.action.speed.value)

        condition: TerminalCondition = self.check_terminal(state=state)
        # print(xe, ye, b, step.action.speed.value, step.action.direction.radians, condition)

        reward = get_reward(
            rules=self._rules, params=self._params, geometry=self._geometry, state=state, condition=condition)
        # print(f"{reward=}")

        self.agent.propagate(
            old_state=state, new_state=real_new_state, action=step.action, reward=reward)

        self.agent.state = real_new_state

        self._wind_manager.update()
        return condition

    def reset(self):
        self.agent.reset()
        self._wind_manager.reset()

    def check_terminal(self, state: State, tick: int = 0) -> TerminalCondition:
        xe, ye = self._geometry.target.x, self._geometry.target.y
        dist = math.dist((state.x, state.y), (xe, ye))

        if (dist < self._rules.rules.terminal.success.max_abs_difference
                and state.b > self._rules.rules.terminal.success.min_b
                and tick < self._rules.rules.terminal.success.max_t):
            return TerminalCondition.SUCCESS
        elif (state.b < self._rules.rules.terminal.fail.max_b
              or tick > self._rules.rules.terminal.fail.min_t):
            return TerminalCondition.FAIL

        return TerminalCondition.NOTHING
