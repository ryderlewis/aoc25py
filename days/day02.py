from .day import Day


class Day02(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        s = set()
        for start, end in self.parse_input():
            s |= self.invalid(start, end, groups=2)
        return str(sum(s))

    def part2(self) -> str:
        s = set()
        for start, end in self.parse_input():
            for g in range(2, len(str(end))+1):
                s |= self.invalid(start, end, groups=g)
        return str(sum(s))

    def parse_input(self) -> list[tuple[int, int]]:
        ret = []
        for x in self.data().strip().split(','):
            a, b = x.split('-')
            ret.append((int(a), int(b)))
        return ret

    def invalid(self, start: int, end: int, groups: int = 2) -> set[int]:
        ret = set()
        while start <= end:
            if len(str(start)) % groups != 0:
                start = int('1' + '0' * (len(str(start))))
                continue

            # split the number in even groups
            left = str(start)[:len(str(start)) // groups]
            invalid = int(left * groups)
            if start <= invalid <= end:
                ret.add(invalid)
            start = int(str(int(left)+1) + '0' * len(left) * (groups - 1))
        return ret