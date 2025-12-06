from .day import Day


class Day04(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rolls = [list(line) for line in self.data_lines()]

    def part1(self) -> str:
        rows = len(self._rolls)
        cols = len(self._rolls[0])

        return str(sum([self.forkliftable(r, c) for r in range(rows) for c in range(cols)]))

    def part2(self) -> str:
        count = 0
        rows = len(self._rolls)
        cols = len(self._rolls[0])

        while True:
            to_remove = []
            for r in range(rows):
                for c in range(cols):
                    if self.forkliftable(r, c):
                        to_remove.append((r, c))
            if not to_remove:
                break
            count += len(to_remove)
            for r, c in to_remove:
                self._rolls[r][c] = '.'

        return str(count)
    
    def has_roll(self, row: int, col: int) -> bool:
        if row < 0 or row >= len(self._rolls):
            return False
        if col < 0 or col >= len(self._rolls[row]):
            return False
        return self._rolls[row][col] == '@'

    def forkliftable(self, row: int, col: int) -> bool:
        if not self.has_roll(row, col):
            return False

        neighbors = sum([1 for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                         if self.has_roll(row + dr, col + dc) and (dr != 0 or dc != 0)])
        return neighbors < 4