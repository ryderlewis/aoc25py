from .day import Day
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int


class Day09(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = [Point(*map(int, line.split(","))) for line in self.data_lines()]

    def part1(self) -> str:
        m = 0
        for i, p1 in enumerate(self.points):
            for p2 in self.points[i+1:]:
                area = (1+abs(p1.x - p2.x)) * (1+abs(p1.y - p2.y))
                m = max(m, area)
        return str(m)

    def part2(self) -> str:
        return "dayXX 2"
