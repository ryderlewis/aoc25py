from functools import lru_cache
from .day import Day
from collections import deque
from dataclasses import dataclass
import sys

@dataclass(frozen=True)
class Machine:
    lights: tuple[bool, ...]
    buttons: tuple[tuple[int, ...], ...]
    joltage: tuple[int, ...]

    def __post_init__(self):
        if any(len(button) != len(set(button)) for button in self.buttons):
            raise ValueError("each button must have unique indices")
        if any(max(button) >= len(self.joltage) for button in self.buttons):
            raise ValueError("button indices must be within joltage range")

    def min_light_presses(self) -> int:
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

    def min_joltage_presses(self) -> int:
        buttons = tuple(sorted(self.buttons, key=lambda x: (-len(x), x)))
        r = self._jp_recur(self.joltage, buttons, fast=True)
        if r > 0:
            print(f"Fast {r}: {self.joltage}")
        else:
            r = self._jp_recur(self.joltage, buttons, fast=False)
            if r < 0:
                raise ValueError(f"{self.state} is bad")
            print(f"Slow {r}: {self.joltage}")
        return r


    @lru_cache(maxsize=None)
    def _jp_recur(self, state: tuple[int, ...], buttons: tuple[tuple[int, ...], ...], fast: bool) -> int:
        # print(f"{state}")
        if max(state) == 0:
            return 0
        min_len = None
        for b in buttons:
            # find number of presses possible with this button
            press_count = min(s for i, s in enumerate(state) if i in b)
            try_count = 1 if fast else 2

            while try_count > 0 and press_count > 0:
                try_count -= 1
                next_state = tuple(s - (press_count if i in b else 0) for i, s in enumerate(state))
                recur_ct = self._jp_recur(next_state, buttons, fast)
                if recur_ct >= 0:
                    if min_len is None or press_count + recur_ct < min_len:
                        min_len = press_count + recur_ct
                if try_count > 0:
                    if press_count > 1:
                        press_count = (press_count+1)//2
                    else:
                        try_count = 0

        if min_len is None:
            return -1
        return min_len

class Day10(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machines = self.parse_input()

    def part1(self) -> str:
        return str(sum(machine.min_light_presses() for machine in self.machines))

    def part2(self) -> str:
        sys.setrecursionlimit(5000)
        return str(sum(machine.min_joltage_presses() for machine in self.machines))

    def parse_input(self) -> list[Machine]:
        ret = []

        for line in self.data_lines():
            parts = line.split()
            lights, *buttons, joltage = parts
            machine = Machine(
                lights=tuple([c == '#' for c in lights[1:-1]]),
                buttons=tuple([tuple(int(x) for x in b[1:-1].split(',')) for b in buttons]),
                joltage=tuple([int(x) for x in joltage[1:-1].split(',')])
            )
            ret.append(machine)
        return ret