from math import exp


def pulse_train(
    bpm: float,
    duration_sec: float,
    sample_rate: int = 44100,
    window_radius: int = 5000,
):
    """
    Generate an easily testable signal for BPM detection. The signal will consist of pulses which are short burts of higher amplitude.
    Improving this by ensuring
        - pulses are wider than frame_size (used in rms_batch)
        - energy needs to be smooth/gaussian (not an on/off square)
        - envelopes have a single maxima per beat

    """
    samples = int(duration_sec * sample_rate)
    signal = [0.0] * samples  # all 0, our pulse will be a 1

    beats_per_sec = bpm / 60.0
    samples_per_beat = int(sample_rate / beats_per_sec)

    sigma = window_radius / 3

    for beat_center in range(0, samples, samples_per_beat):
        # center of the "beat"
        # distribute energy with max at center and min at -spread and +spread
        # energy != linear distance from center but gaussian
        # energy = exp(-(distance ** 2) / (2 * sigma ** 2))
        # signal[idx] += energy
        for offset in range(window_radius):
            energy = exp(-(offset**2) / (2 * sigma**2))
            # calculate energy left of center of the beat_center
            idx = beat_center - offset
            if idx > -1:
                signal[idx] += energy

            # calculate energy right of center of the beat_center
            idx = beat_center + offset
            if idx < samples:
                signal[idx] += energy

    return signal
