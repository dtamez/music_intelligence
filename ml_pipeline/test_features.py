from synthetic_signals import pulse_train
from features import detect_peaks
from rust_bridge import rms_batch


def test_pulse_train_20_peaks_at_120_bpm():
    bpm = 120  # 2 beats per second
    duration_sec = 10

    signal = pulse_train(bpm=bpm, duration_sec=duration_sec)

    rms_envelope = rms_batch(signal, 1024, 512)
    peaks = detect_peaks(rms_envelope)
    assert len(peaks) == 20
