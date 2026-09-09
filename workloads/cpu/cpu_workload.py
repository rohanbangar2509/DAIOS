import time


def cpu_workload(duration=60):
    print(f"Starting CPU-bound workload for {duration} seconds...")

    end_time = time.time() + duration

    number = 2

    while time.time() < end_time:
        is_prime = True

        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                is_prime = False
                break

        number += 1

    print("CPU workload completed.")


if __name__ == "__main__":
    cpu_workload()
