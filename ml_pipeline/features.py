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


def detect_peaks(rms_envelope):
    # takes an array of values and outputs a subset of those values
    # a value counts as a peak if it is greater than both
    # the previous and the subsequnent sample
    output = []
    for idx, val in enumerate(rms_envelope):
        if idx == 0 or idx == len(rms_envelope) - 1:
            continue
        if val > rms_envelope[idx - 1] and val > rms_envelope[idx + 1]:
            output.append(idx)
    return output
