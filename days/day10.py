from functools import lru_cache
from .day import Day
from collections import deque
from dataclasses import dataclass
from itertools import product
import sympy as sp

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
        vars = sp.symbols(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')[:len(self.buttons)], integer=True)

        inputs = []
        for i in range(len(self.joltage)):
            inputs.append([(1 if i in b else 0) for b in self.buttons])

        M = sp.Matrix(inputs)
        b = sp.Matrix(self.joltage)

        rref_aug, pivots = M.row_join(b).rref()

        # Free variable indices among the 8 variable columns (ignore RHS col)
        free_vars = [vars[i] for i in range(len(vars)) if i not in pivots]

        debug = len(free_vars) > 2
        if debug:
            print(self)
            print(inputs)
            print("Pivot columns:", pivots)
            print("RREF:", rref_aug)
            print("Free variables:", free_vars)

        # Solve symbolically (may return expressions involving free variables like H)
        sol_set = sp.linsolve((M, b), vars)
        (sol_tuple,) = list(sol_set)
        exprs = list(sol_tuple)

        S = sp.simplify(sum(exprs))

        def is_nonneg_int(val):
            val = sp.simplify(val)
            return val.is_integer and val >= 0

        best = None

        # Search range for each free variable.
        # For your case with H free, H is small because G >= 0 forces H <= 2 (odd => 1),
        # but we'll just search a bit wider safely.
        # print(f"RYDER: {max(self.joltage)}")
        search_ranges = [range(0, max(self.joltage)+1) for _ in free_vars]

        for ct, free_vals in enumerate(product(*search_ranges), 1):
            subs = dict(zip(free_vars, free_vals))
            point = [sp.simplify(e.subs(subs)) for e in exprs]

            if debug and ct % 1_000_000 == 0:
                print(f"RYDER: tested {ct}")

            if all(is_nonneg_int(v) for v in point):
                s_val = sp.simplify(S.subs(subs))
                if best is None or s_val < best:
                    best = s_val
                    if len(free_vars) > 2:
                        print(f"RYDER: found {best}")

        if debug:
            print("Min sum =", best)
        return best

class Day10(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machines = self.parse_input()

    def part1(self) -> str:
        return str(sum(machine.min_light_presses() for machine in self.machines))

    def part2(self) -> str:
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