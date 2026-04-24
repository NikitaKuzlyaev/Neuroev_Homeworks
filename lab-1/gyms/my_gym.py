import math

from agents.agent import Agent
from agents.common.geometry import GeometryFunctions
from agents.common.wind import WindManager
from bootstraps.key_registry import StorageKey
from framework.context import Context
from gyms.gym import Gym, TerminalCondition
from politics.states.state import State
from schemas.action import Action
from schemas.agent import StepResponse
from schemas.geometry import GeometryConfig
from schemas.params import ParamsConfig
from schemas.rules import RulesConfig, ElseAward


class MyGym(Gym):

    def __init__(self, context: Context, agent: Agent):
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
        xn, yn = self._get_new_xy(state=state, action=step.action)

        xe, ye = GeometryFunctions.get_next_position(x1=state.x, y1=state.y, x2=xn, y2=yn, geometry=self._geometry)

        # print("VV", math.dist((state.x, state.y), (xe, ye)))
        b = self._get_new_b(state=state)

        real_new_state = State(x=xe, y=ye, b=b, v=step.action.speed.value)

        condition: TerminalCondition = self.check_terminal(state=state)  # todo
        # print(xe, ye, b, step.action.speed.value, step.action.direction.radians, condition)
        reward = self._get_reward(state=state, condition=condition)

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

    def _get_new_xy(self, state: State, action: Action) -> tuple[float, float]:
        x = state.x + action.speed.value * math.cos(action.direction.radians) + self._wind_manager.wx
        y = state.y + action.speed.value * math.sin(action.direction.radians) + self._wind_manager.wy
        return x, y

    def _get_new_b(self, state: State) -> float:
        _I = int(self._is_inside_charge_area(state))

        speed_coef = self._params.agent.battery.speed_coef
        wind_x_coef = self._params.agent.battery.wind_x_coef
        wind_y_coef = self._params.agent.battery.wind_y_coef
        charge_coef = self._params.agent.battery.charge_coef
        wx = self._wind_manager.wx
        wy = self._wind_manager.wy

        b = min(1.0,
                state.b + speed_coef * state.v ** 2 + wind_x_coef * abs(wx) + wind_y_coef * abs(wy) + _I * charge_coef)
        return b

    def _is_inside_charge_area(self, state: State) -> bool:
        I = math.dist(
            (state.x, state.y),
            (self._geometry.target.x, self._geometry.target.y)
        ) < self._geometry.target.r
        return I

    def _get_reward(self, state: State, condition: TerminalCondition) -> float:
        if condition == TerminalCondition.SUCCESS:
            reward = self._rules.rules.award.success
        elif condition == TerminalCondition.FAIL:
            reward = self._rules.rules.award.fail
        else:
            ea: ElseAward = self._rules.rules.award.else_
            _I = self._is_inside_charge_area(state=state)

            reward = (ea.base
                      + ea.speed_coef * state.v ** 2
                      + ea.I_station_coef * self._params.agent.battery.charge_coef * int(_I)
                      )

        return reward
