from .day import Day


class Day03(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        return str(sum([self.joltage(line, 2) for line in self.data_lines()]))

    def part2(self) -> str:
        return str(sum([self.joltage(line, 12) for line in self.data_lines()]))

    def joltage(self, line: str, digits: int) -> int:
        if digits == 1:
            return int(max(line))

        max_dig = -1
        dig_pos = -1

        for i, c in enumerate(line[:-(digits-1)]):
            dig = int(c)
            if dig > max_dig:
                max_dig = dig
                dig_pos = i
        
        return max_dig * 10**(digits-1) + self.joltage(line[dig_pos+1:], digits-1)