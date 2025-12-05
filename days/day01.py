from .day import Day


class Day01(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        pos = 50
        count = 0

        for line in self.data_lines():
            steps = int(line[1:])
            if line[0] == 'L':
                steps = -steps
            pos += steps
            pos %= 100
            if pos == 0:
                count += 1

        return str(count)

    def part2(self) -> str:
        pos = 50
        count = 0

        for line in self.data_lines():
            steps = int(line[1:])
            if steps == 0:
                continue

            if line[0] == 'L':
                steps = -steps
                if pos == 0:
                    pos = 100
            
            while steps < 0:
                if pos + steps > 0:
                    pos += steps
                    steps = 0
                else:
                    count += 1
                    steps += pos
                    pos = 100 if steps < 0 else 0

            while steps > 0:
                if pos + steps < 100:
                    pos += steps
                    steps = 0
                else:
                    count += 1
                    steps -= (100 - pos)
                    pos = 0

        return str(count)
