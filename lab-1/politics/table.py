class Table:

    def __init__(self, state_size: int, action_size: int):
        self.state_size = state_size
        self.action_size = action_size
        self.table = [[0.0 for _ in range(action_size)] for _ in range(state_size)]

    def get(self, state_idx: int, action_idx: int) -> float:
        return self.table[state_idx][action_idx]

    def set(self, state_idx: int, action_idx: int, value: float) -> None:
        self.table[state_idx][action_idx] = value

    def row(self, state_idx: int) -> list[float]:
        return self.table[state_idx]

    def max_value(self, state_idx: int) -> float:
        return max(self.table[state_idx])

    def best_action(self, state_idx: int) -> int:
        row = self.table[state_idx]
        best_idx = 0
        best_val = row[0]

        for idx, value in enumerate(row):
            if value > best_val:
                best_val = value
                best_idx = idx

        return best_idx
