import time


def memory_workload(duration=60):
    print(f"Starting memory-bound workload for {duration} seconds...")

    # Allocate approximately 500 MB.
    data = bytearray(500 * 1024 * 1024)

    # Touch the memory so the allocation is actually used.
    for i in range(0, len(data), 4096):
        data[i] = 1

    end_time = time.time() + duration

    while time.time() < end_time:

        for i in range(0, len(data), 4096):
            data[i] = (data[i] + 1) % 256

    print("Memory workload completed.")


if __name__ == "__main__":
    memory_workload()
