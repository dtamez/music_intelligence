from math import exp


def pulse_train(
    bpm: float,
    duration_sec: float,
    sample_rate: int = 44100,
    window_radius: int = 5000,
    sigma_ratio: float = 3.0,
    frame_size: int = 1024,
):
    """
    Generate a deterministic, BPM accurate, RMS detectable test signal for validating.
    Energy for each beat: E(d) = exp(-(d²) / (2σ²))
    Energy is applied ov [-window_radius, +window_radius]
    """
    # shift the centers of the beats
    beat_region_samples = int(duration_sec * sample_rate)  # length w/o the padding
    padding = max(window_radius, frame_size)
    total_samples = beat_region_samples + (2 * padding)

    beat_start = padding  # after the padding

    signal = [0.0] * total_samples

    beats_per_sec = bpm / 60.0
    samples_per_beat = int(sample_rate / beats_per_sec)

    sigma = window_radius / sigma_ratio

    num_beats = int(round(duration_sec * beats_per_sec))
    for n in range(num_beats):
        beat_center = beat_start + int(n * samples_per_beat)
        for offset in range(-window_radius, window_radius + 1):
            idx = beat_center + offset

            if 0 <= idx < total_samples:
                energy = exp(-(offset**2) / (2 * sigma**2))
                signal[idx] += energy

    return signal
