import rust_audio


"""
Thin Python wrapper around Rust.
"""


def sum_values(values):
    return rust_audio.sum_values(values)


def get_energy(audio_frame):
    return rust_audio.rms_energy(audio_frame)
