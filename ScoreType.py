from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(self, start, count, last_values):
        return self


class ScoreType(AutoName):
    LINEAR = auto()
    POWER = auto()
    EXPONENTIAL = auto()