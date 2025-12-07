from .day import Day
from functools import lru_cache


class Day07(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lines = self.data_lines()

    def part1(self) -> str:
        beams = set()
        count = 0
        for line in self._lines:
            for i, c in enumerate(line):
                if c == 'S':
                    beams.add(i)
                elif c == '^' and i in beams:
                    count += 1
                    beams.remove(i)
                    beams.add(i-1)
                    beams.add(i+1)
        return str(count)

    def part2(self) -> str:
        beam_col = self._lines[0].index('S')
        return str(self.timelines(1, beam_col))

    @lru_cache(maxsize=None)
    def timelines(self, row: int, col: int) -> int:
        while row < len(self._lines):
            c = self._lines[row][col]
            if c == '^':
                return self.timelines(row + 1, col - 1) + self.timelines(row + 1, col + 1)
            else:
                row += 1
        return 1
