def frame_signal(signal, frame_size: int, hop_size: int):
    """
    Split signal into overlapping frames.
    """
    frames = []
    for i in range(0, len(signal) - frame_size + 1, hop_size):
        frames.append(signal[i : i + frame_size])
    return frames
