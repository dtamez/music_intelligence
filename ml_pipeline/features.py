from rust_bridge import sum_values, get_energy
import math


def python_sum(values):
    return sum(values)


def rust_sum(values):
    return sum_values(values)


def python_rms(values):
    return math.sqrt(sum(v * v for v in values) / len(values))


def rust_rms(values):
    return get_energy(values)
