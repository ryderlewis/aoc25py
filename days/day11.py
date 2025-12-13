from functools import lru_cache
from .day import Day
from dataclasses import dataclass

@dataclass
class Device:
    name: str
    outputs: tuple[Device, ...]


class Day11(Day):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.devices = self._parse_devices()

    def part1(self) -> str:
        """
        Count the number of paths from device "you" to device "out".
        """
        return str(self.count("you", "out", dac=True, fft=True))

    def part2(self) -> str:
        return str(self.count("svr", "out", dac=False, fft=False))
    
    @lru_cache(None)
    def count(self, start: str, end: str, dac: bool, fft: bool) -> int:
        if start == "dac":
            dac = True
        if start == "fft":
            fft = True
        if start == end:
            return 1 if dac and fft else 0
        dev = self.devices[start]
        return sum(self.count(out.name, end, dac, fft) for out in dev.outputs)

    def _parse_devices(self) -> dict[str, Device]:
        ret = {}
        tmp: dict[str, list[str]] = {}
        for line in self.data_lines():
            name, outs = line.split(": ")
            tmp[name] = outs.split()
            ret[name] = Device(name, ())

        ret["out"] = Device("out", ())
        for name, outs in tmp.items():
            ret[name].outputs = tuple(ret[out] for out in outs)
        return ret
        