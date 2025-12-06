from .day import Day
from dataclasses import dataclass

@dataclass
class Range:
    start: int
    end: int

@dataclass(frozen=True)
class InputData:
    fresh_ranges: list[Range]
    ingredients: list[int]


class Day05(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def part1(self) -> str:
        input = self.parse_input()
        count = 0
        for ingredient in input.ingredients:
            for r in input.fresh_ranges:
                if r.start <= ingredient <= r.end:
                    count += 1
                    break
        return str(count)

    def part2(self) -> str:
        input = self.parse_input()

        combined = []
        for r in sorted(input.fresh_ranges, key=lambda x: x.start):
            if not combined or r.start > combined[-1].end:
                combined.append(r)
            else:
                combined[-1].end = max(combined[-1].end, r.end)

        return str(sum([c.end-c.start+1 for c in combined]))

    def parse_input(self) -> InputData:
        lines = self.data_lines()
        fresh_ranges = []
        ingredients = []

        parsing_fresh = True
        for line in lines:
            if line == "":
                parsing_fresh = False
                continue

            if parsing_fresh:
                parts = line.split("-")
                fresh_ranges.append(Range(int(parts[0]), int(parts[1])))
            else:
                ingredients.append(int(line))

        return InputData(fresh_ranges=fresh_ranges, ingredients=ingredients)