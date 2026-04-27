class Table:

    def __init__(self, n_states: int, n_actions: int):
        """"""
        self.q = [[0.0 for _ in range(n_actions)] for _ in range(n_states)]

    def set(self, state_idx: int, action_idx: int, value: float):
        """"""
        self.q[state_idx][action_idx] = value

    def get(self, state_idx: int, action_idx: int):
        """"""
        return self.q[state_idx][action_idx]

    def best_action(self, state_idx: int) -> int:
        """"""
        return max(
            range(len(self.q[state_idx])),
            key=lambda action_idx: self.q[state_idx][action_idx]
        )
