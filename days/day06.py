from .day import Day
from functools import reduce


class Day06(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        cols = self.parse_columns()
        return str(self.solve(cols))

    def part2(self) -> str:
        cols = self.parse_columns_2()
        return str(self.solve(cols))
    
    def solve(self, cols: list[list[str]]) -> int:
        total = 0
        for col in cols:
            if col[-1] == '+':
                total += sum(int(x) for x in col[:-1])
            elif col[-1] == '*':
                total += reduce(lambda a, b: a * b, (int(x) for x in col[:-1]), 1)
            else:
                raise ValueError(f"Unknown operator {col[-1]}")
        return total

    def parse_columns(self) -> list[list[str]]:
        ret = []
        for line in self.data_lines():
            vals = line.strip().split()
            if not ret:
                ret = [[] for _ in vals]
            for i, v in enumerate(vals):
                ret[i].append(v)
        return ret

    def parse_columns_2(self) -> list[list[str]]:
        lines = self.data_lines()
        # fix self.data_lines() trimming the last line
        while len(lines[-1]) < len(lines[0]):
            lines[-1] += ' '

        operator = None
        ret = []

        for col in range(len(lines[0])):
            if (op := lines[-1][col]) != ' ':
                operator = op
                ret.append([])
            num = ''.join([lines[row][col] for row in range(len(lines)-1)]).strip()
            if num:
                ret[-1].append(num)
            elif operator is not None:
                ret[-1].append(operator)
                operator = None
        
        ret[-1].append(operator)
        return ret