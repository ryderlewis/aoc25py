from .day import Day


class Day07(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        beams = set()
        count = 0
        for line in self.data_lines():
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
        return "dayXX 2"
