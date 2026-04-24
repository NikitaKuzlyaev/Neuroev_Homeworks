from gyms.gym import TerminalCondition
from politics.states.state import State
from rules.charge import is_inside_charge_area
from schemas.geometry import GeometryConfig
from schemas.params import ParamsConfig
from schemas.rules import ElseAward, RulesConfig


def get_reward(
        rules: RulesConfig,
        params: ParamsConfig,
        geometry: GeometryConfig,
        state: State,
        condition: TerminalCondition
) -> float:
    """"""
    if condition == TerminalCondition.SUCCESS:
        reward = rules.rules.award.success
    elif condition == TerminalCondition.FAIL:
        reward = rules.rules.award.fail
    else:
        ea: ElseAward = rules.rules.award.else_
        _I = is_inside_charge_area(state=state, geometry=geometry)

        reward = (ea.base
                  + ea.speed_coef * state.v ** 2
                  + ea.I_station_coef * params.agent.battery.charge_coef * int(_I)
                  )

    return reward
