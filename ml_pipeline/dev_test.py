from features import python_rms, rust_rms
import random
import time

data = [random.random() for _ in range(500_000)]

t0 = time.time()
p = python_rms(data)
t1 = time.time()

r = rust_rms(data)
t2 = time.time()

print(f"Python rms: {p} time: {t1 - t0}")
print(f"Rust rms: {r} time: {t2 - t1}")
