from synthetic_signals import pulse_train
from features import python_rms, detect_peaks
from visualization import plot_signal_and_rms
from rust_bridge import rms_batch

bpm = 120
signal = pulse_train(bpm=bpm, duration_sec=10)

frame_size = 1024
hop_size = 512
rms_envelope = rms_batch(signal, frame_size, hop_size)

peaks = detect_peaks(rms_envelope)

print(peaks[:10])
print("Total peaks:", len(peaks))

for i in peaks[:5]:
    print(rms_envelope[i - 2 : i + 3])

# plot_signal_and_rms(
#     signal,
#     rms_envelope,
#     hop_size=hop_size,
#     title="Synthetic Beat Signal + RMS Envelope",
# )

# energy = rms_batch(signal, frame_size, hop_size)
#
# print(f"Energy frames: {energy[:20]}")
# print(f"Frames: {len(energy)}")
