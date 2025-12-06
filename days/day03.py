from .day import Day


class Day03(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        return str(sum([self.joltage(line) for line in self.data_lines()]))

    def part2(self) -> str:
        return "dayXX 2"

    def joltage(self, line: str) -> int:
        max_dig = -1
        dig_pos = -1

        for i, c in enumerate(line[:-1]):
            dig = int(c)
            if dig > max_dig:
                max_dig = dig
                dig_pos = i
        
        return max_dig * 10 + int(max(line[dig_pos + 1:]))