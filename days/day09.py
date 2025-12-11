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
        min_x = min(p.x for p in self.points)
        max_x = max(p.x for p in self.points)
        min_y = min(p.y for p in self.points)
        max_y = max(p.y for p in self.points)

        border_points = set()
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i+1) % len(self.points)]

            if p1.x == p2.x:
                for y in range(min(p1.y, p2.y), max(p1.y, p2.y) + 1):
                    border_points.add(Point(p1.x, y))
            elif p1.y == p2.y:
                for x in range(min(p1.x, p2.x), max(p1.x, p2.x) + 1):
                    border_points.add(Point(x, p1.y))
            else:
                raise ValueError("Points must form axis-aligned edges")
        
        out_p = Point(min_x - 1, min_y - 1)
        outside_points = set()
        visited = set()
        to_visit = [out_p]
        print(f"Border area: {len(border_points)}")

        while to_visit:
            p = to_visit.pop()
            if p in visited or p in border_points:
                continue
            visited.add(p)
            outside_points.add(p)

            neighbors = [
                Point(p.x + 1, p.y),
                Point(p.x - 1, p.y),
                Point(p.x, p.y + 1),
                Point(p.x, p.y - 1),
            ]
            for n in neighbors:
                if (min_x - 1 <= n.x <= max_x + 1 and min_y - 1 <= n.y <= max_y + 1):
                    to_visit.append(n)

        print(f"Outside area: {len(outside_points)}")
        return ""