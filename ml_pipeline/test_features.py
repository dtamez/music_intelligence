import pytest
from synthetic_signals import pulse_train
from features import detect_peaks
from rust_bridge import rms_batch
from dataclasses import dataclass


@dataclass
class TestSignalConfig:
    bpm: float
    duration_sec: float
    sample_rate: int = 41000

    # kernel geometry
    window_radius: int = 5000
    sigma_ratio: float = 3.0  # sigma -> window_radius / sigma_ratio

    # padding geometry
    padding: int = 5000

    # feature geometry
    frame_size: int = 1024
    hop_size: int = 512


def generate_test_signal(cfg: TestSignalConfig) -> list[float]:
    signal = pulse_train(
        bpm=cfg.bpm,
        duration_sec=cfg.duration_sec,
        sample_rate=cfg.sample_rate,
        window_radius=cfg.window_radius,
        sigma_ratio=cfg.sigma_ratio,
        padding=cfg.padding,
    )

    return signal


def extract_features(signal: list[float], cfg: TestSignalConfig):
    rms = rms_batch(signal, cfg.frame_size, cfg.hop_size)
    peaks = detect_peaks(rms)
    return rms, peaks


@pytest.mark.parametrize(
    "bpm,duration,expected_beats",
    [
        (60, 10, 10),
        (120, 10, 20),
        (90, 10, 15),
        (120, 5, 10),
        (120, 20, 40),
    ],
)
def test_peak_count_invariant(bpm, duration, expected_beats):
    cfg = TestSignalConfig(bpm=bpm, duration_sec=duration)

    signal = generate_test_signal(cfg)
    rms, peaks = extract_features(signal, cfg)

    assert len(peaks) == expected_beats
