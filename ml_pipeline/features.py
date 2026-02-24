from rust_bridge import sum_values, get_energy
import math


def python_sum(values):
    return sum(values)


def rust_sum(values):
    return sum_values(values)


def python_rms(values, frame_size, hop_size):
    out = []

    i = 0
    while i + frame_size <= len(values):
        frame = values[i : i + frame_size]
        sum_sq = 0.0
        for val in frame:
            sum_sq += val**2

        rms = math.sqrt(sum_sq / frame_size)
        out.append(rms)
        i += hop_size

    return out


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
