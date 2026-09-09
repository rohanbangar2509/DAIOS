import psutil
import time


def get_process_info(process):
    try:
        with process.oneshot():
            return {
                "pid": process.pid,
                "name": process.name(),
                "cpu_percent": process.cpu_percent(),
                "memory_percent": process.memory_percent(),
                "status": process.status(),
                "num_threads": process.num_threads(),
            }

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


def monitor_processes(interval=2):
    while True:
        print("\n" + "=" * 80)
        print("DAIOS PROCESS TELEMETRY")
        print("=" * 80)

        processes = []

        for process in psutil.process_iter():
            info = get_process_info(process)

            if info:
                processes.append(info)

        processes.sort(
            key=lambda x: x["cpu_percent"],
            reverse=True
        )

        print(
            f"{'PID':<8}"
            f"{'NAME':<25}"
            f"{'CPU %':<10}"
            f"{'MEM %':<10}"
            f"{'THREADS':<10}"
            f"{'STATUS':<15}"
        )

        print("-" * 80)

        for process in processes[:15]:
            print(
                f"{process['pid']:<8}"
                f"{process['name'][:24]:<25}"
                f"{process['cpu_percent']:<10.2f}"
                f"{process['memory_percent']:<10.2f}"
                f"{process['num_threads']:<10}"
                f"{process['status']:<15}"
            )

        time.sleep(interval)


if __name__ == "__main__":
    monitor_processes()
