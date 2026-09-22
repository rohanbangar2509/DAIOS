import time
import numpy as np

DURATION = 60
MEMORY_SIZE_MB = 1000


def memory_workload(duration=DURATION):
    print(
        f"Starting memory-bound workload for "
        f"{duration} seconds..."
    )

    # Allocate a large working set
    size = (MEMORY_SIZE_MB * 1024 * 1024) // 8

    data = np.zeros(size, dtype=np.float64)

    print(
        f"Allocated approximately "
        f"{data.nbytes / (1024 * 1024):.0f} MB"
    )

    # Touch the memory so physical pages are allocated
    data[:] = 1.0

    end_time = time.time() + duration

    while time.time() < end_time:

        # Strided memory access.
        # This forces repeated memory reads/writes
        # without a Python-level loop over every element.
        data[::64] += 1.0

    print("Memory workload completed.")


if __name__ == "__main__":
    memory_workload()