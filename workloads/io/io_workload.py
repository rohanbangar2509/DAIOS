import os
import time


FILE_PATH = "workloads/io/test_data.bin"


def io_workload(duration=60):
    print(f"Starting I/O-bound workload for {duration} seconds...")

    end_time = time.time() + duration

    chunk = os.urandom(1024 * 1024)  # 1 MB

    with open(FILE_PATH, "wb") as file:

        while time.time() < end_time:
            file.write(chunk)
            file.flush()
            os.fsync(file.fileno())

    print("I/O workload completed.")


if __name__ == "__main__":
    io_workload()
