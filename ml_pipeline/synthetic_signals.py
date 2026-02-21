def pulse_train(
    bpm: float,
    duration_sec: float,
    sample_rate: int = 44100,
    pulse_width_ms: float = 10.0,
):
    """
    Generate an easily testable signal for BPM detection. The signal will consist of pulses which are short burts of higher amplitude.
    """
    samples = int(duration_sec * sample_rate)
    signal = [0.0] * samples  # all 0, our pulse will be a 1

    beats_per_sec = bpm / 60.0
    samples_per_beat = int(sample_rate / beats_per_sec)
    # how many samples will contain the burst
    pulse_width_samples = int((pulse_width_ms / 1000.0) * sample_rate)

    for i in range(0, samples, samples_per_beat):
        for j in range(pulse_width_samples):
            if i + j < samples:  # prevent IndexError
                signal[i + j] = 1.0  # pulse

    return signal
