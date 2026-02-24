import pytest
from synthetic_signals import pulse_train
from features import detect_peaks, python_rms
from rust_bridge import rms_batch
from dataclasses import dataclass


"""
Peak count wrong                geometry bug
Spacing wrong                   timing bug
RMS shape wrong                 window/kernel mismatch 
Cross-lang diff                 numeric/typing bug 
Boundary peaks missing          padding bug 
Merged peaks                    kernel overlap bug 
Drift                           cumulative error
"""


@dataclass
class TestSignalConfig:
    bpm: float
    duration_sec: float
    sample_rate: int = 41000

    # kernel geometry
    window_radius: int = 5000
    sigma_ratio: float = 3.0  # sigma -> window_radius / sigma_ratio

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
        frame_size=cfg.frame_size,
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


def test_peak_spacing_uniformity():
    cfg = TestSignalConfig(bpm=120, duration_sec=10.0)

    signal = generate_test_signal(cfg)
    rms, peaks = extract_features(signal, cfg)

    diffs = [peaks[i + 1] - peaks[i] for i in range(len(peaks) - 1)]
    mean = sum(diffs) / len(diffs)

    # every spacing must be within +2 or -2 frames of the avg spacing
    for d in diffs:
        assert abs(d - mean) < 2


def test_python_rust_rms_equivalence():
    cfg = TestSignalConfig(bpm=120, duration_sec=10)
    signal = generate_test_signal(cfg)

    rms_rust = rms_batch(signal, cfg.frame_size, cfg.hop_size)
    rms_py = python_rms(signal, cfg.frame_size, cfg.hop_size)

    for r, p in zip(rms_rust, rms_py):
        assert abs(r - p) < 1e-6  # floating point tolerance
