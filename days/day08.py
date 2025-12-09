from .day import Day
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    idx: int
    x: int
    y: int
    z: int

@dataclass(frozen=True)
class PointPair:
    p1: Point
    p2: Point

    @property
    def dist(self) -> float:
        return ((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2 + (self.p1.z - self.p2.z) ** 2) ** 0.5

@dataclass
class Circuit:
    idx: int
    points: set[Point]

    @property
    def size(self) -> int:
        return len(self.points)

class Day08(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = self.parse()

    def part1(self) -> str:
        pairs: list[PointPair] = []
        for i, p1 in enumerate(self.points):
            for p2 in self.points[i+1:]:
                pairs.append(PointPair(p1, p2))

        pairs.sort(key=lambda d: d.dist)
        dsize = 1000 if len(self.points) >= 1000 else 10

        circuits = {p.idx: Circuit(p.idx, points={p}) for p in self.points}

        for pair in pairs[:dsize]:
            c1 = circuits[pair.p1.idx]
            c2 = circuits[pair.p2.idx]

            c1.points |= c2.points
            for p in c1.points:
                circuits[p.idx] = c1
        
        unique_circuits = {c.idx: c for c in circuits.values()}
        top3 = sorted(unique_circuits.values(), key=lambda c: -len(c.points))

        ans = top3[0].size * top3[1].size * top3[2].size
        return str(ans)

    def part2(self) -> str:
        pairs: list[PointPair] = []
        for i, p1 in enumerate(self.points):
            for p2 in self.points[i+1:]:
                pairs.append(PointPair(p1, p2))

        pairs.sort(key=lambda d: d.dist)
        dsize = 1000 if len(self.points) >= 1000 else 10

        circuits = {p.idx: Circuit(p.idx, points={p}) for p in self.points}
        circuits_left = set(circuits.keys())

        for pair in pairs:
            c1 = circuits[pair.p1.idx]
            c2 = circuits[pair.p2.idx]

            if c1.idx == c2.idx:
                continue

            if c1.idx > c2.idx:
                c1, c2 = c2, c1

            c1.points |= c2.points
            for p in c1.points:
                circuits[p.idx] = c1
            
            circuits_left.discard(c2.idx)
            if len(circuits_left) == 1:
                return str(pair.p1.x * pair.p2.x)

    def parse(self) -> list[Point]:
        points = []
        for i, line in enumerate(self.data_lines()):
            x, y, z = map(int, line.split(","))
            points.append(Point(i, x, y, z))
        return points