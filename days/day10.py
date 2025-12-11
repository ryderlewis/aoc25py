from .day import Day
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Machine:
    lights: tuple[bool, ...]
    buttons: list[tuple[int, ...]]
    joltage: list[int]

    def min_presses(self) -> int:
        state = tuple([False for _ in range(len(self.lights))])
        count = 0

        d = deque()
        d.append((state, count))
        seen = {state}

        while d:
            state, count = d.popleft()
            if state == self.lights:
                return count

            for button in self.buttons:
                new_state = tuple([(not s if i in button else s) for i, s in enumerate(state)])
                if new_state not in seen:
                    seen.add(new_state)
                    d.append((new_state, count + 1))


class Day10(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machines = self.parse_input()

    def part1(self) -> str:
        return str(sum(machine.min_presses() for machine in self.machines))

    def part2(self) -> str:
        return "dayXX 2"

    def parse_input(self) -> list[Machine]:
        ret = []

        for line in self.data_lines():
            parts = line.split()
            lights, *buttons, joltage = parts
            machine = Machine(
                lights=tuple([c == '#' for c in lights[1:-1]]),
                buttons=[tuple(int(x) for x in b[1:-1].split(',')) for b in buttons],
                joltage=[int(x) for x in joltage[1:-1].split(',')]
            )
            ret.append(machine)
        return ret