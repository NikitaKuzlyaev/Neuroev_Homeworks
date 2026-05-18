import math

from agents.agent import Agent
from agents.common.geometry import GeometryFunctions
from agents.common.wind import WindManager
from bootstraps.key_registry import StorageKey
from evaluation.datacollectors.datacollector import datacollector
from framework.context import Context
from gyms.gym import (
    Gym,
    TerminalCondition, TerminalResult,
)
from politics.states.state import State
from rules.charge import is_inside_charge_area
from rules.movement import (
    get_new_xy,
    get_new_b,
)
from rules.reward import get_reward
from schemas.agent import StepResponse
from schemas.geometry import GeometryConfig
from schemas.params import ParamsConfig
from schemas.rules import RulesConfig
from utils.math_funcs import MathFunctions


class MyGym(Gym):

    def __init__(self, context: Context, agent: Agent):
        """"""
        super().__init__(context, agent)
        self.context = context
        self.agent = agent
        self._geometry: GeometryConfig = context.get(StorageKey.GEO.value)
        self._params: ParamsConfig = context.get(StorageKey.PARAMS.value)
        self._rules: RulesConfig = context.get(StorageKey.RULES.value)
        self._wind_manager: WindManager = WindManager(context=context)

        self.reset()

    @datacollector(
        path="agent.state",
        callback=collector.collect_state,
    )
    def step(self, validate, tick) -> TerminalResult:
        """"""
        step: StepResponse = self.agent.step()
        state: State = self.agent.state

        new_state, hit_t = self._get_new_agent_state(
            step=step, state=state, params=self._params, geometry=self._geometry, wind_manager=self._wind_manager
        )
        self.agent.state = new_state

        condition: TerminalCondition = self.check_terminal(state=new_state)

        reward = get_reward(
            rules=self._rules, params=self._params, geometry=self._geometry, state=new_state, condition=condition,
        )

        self.agent.propagate(
            old_state=state, new_state=new_state, action=step.action, reward=reward,
            done=condition != TerminalCondition.NOTHING,
        )

        self._wind_manager.update()

        return TerminalResult(condition=condition, metrics={"collisions": int(1.0 - hit_t > 0.001)})

    def reset(self) -> None:
        """"""
        self.agent.reset()
        self._wind_manager.reset()

    def check_terminal(self, state: State, tick: int = 0) -> TerminalCondition:
        """"""
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

    def _get_new_agent_state(
            self, step: StepResponse, state: State, params: ParamsConfig, geometry: GeometryConfig,
            wind_manager: WindManager
    ) -> tuple[State, float]:
        """"""
        xe, ye, hit_t = self._get_next_agent_position(state=state, step=step)

        b = get_new_b(
            state=state, params=self._params, geometry=self._geometry, wind_manager=self._wind_manager
        )
        state = State(x=xe, y=ye, b=b, v=step.action.speed.value)
        self._update_agent_battery(state=state, geometry=self._geometry, params=self._params)
        return state, hit_t

    def _get_next_agent_position(
            self, state: State, step: StepResponse
    ) -> tuple[float, float, float]:
        """"""
        xn, yn = get_new_xy(
            state=state, action=step.action, wind_manager=self._wind_manager
        )
        xe, ye, hit_t = GeometryFunctions.get_next_position(
            x1=state.x, y1=state.y, x2=xn, y2=yn, geometry=self._geometry
        )
        return xe, ye, hit_t

    def _update_agent_battery(
            self, state: State, geometry: GeometryConfig, params: ParamsConfig,
    ) -> None:
        """"""
        if is_inside_charge_area(state=state, geometry=geometry):
            state.b = MathFunctions.clip_right(
                state.b + params.agent.battery.charge_coef, params.agent.battery.max_value
            )
        return
