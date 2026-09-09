import csv
import os
import time
from datetime import datetime

import psutil


OUTPUT_FILE = "telemetry/process_telemetry.csv"
INTERVAL = 2


def collect_process_info(process):
    try:
        with process.oneshot():

            cpu_percent = process.cpu_percent()

            memory_percent = process.memory_percent()

            io_read = 0
            io_write = 0

            try:
                io = process.io_counters()
                io_read = io.read_bytes
                io_write = io.write_bytes
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

            try:
                context_switches = process.num_ctx_switches()
                voluntary_switches = context_switches.voluntary
                involuntary_switches = context_switches.involuntary
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                voluntary_switches = 0
                involuntary_switches = 0

            return {
                "timestamp": datetime.now().isoformat(),
                "pid": process.pid,
                "name": process.name(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "io_read_bytes": io_read,
                "io_write_bytes": io_write,
                "voluntary_context_switches": voluntary_switches,
                "involuntary_context_switches": involuntary_switches,
                "num_threads": process.num_threads(),
                "status": process.status(),
            }

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


def initialize_csv():

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    if not os.path.exists(OUTPUT_FILE):

        fields = [
            "timestamp",
            "pid",
            "name",
            "cpu_percent",
            "memory_percent",
            "io_read_bytes",
            "io_write_bytes",
            "voluntary_context_switches",
            "involuntary_context_switches",
            "num_threads",
            "status",
        ]

        with open(OUTPUT_FILE, "w", newline="") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fields
            )

            writer.writeheader()


def monitor_processes():

    initialize_csv()

    print("DAIOS Telemetry Collector Started")
    print(f"Writing telemetry to: {OUTPUT_FILE}")
    print("Press Ctrl+C to stop.\n")

    while True:

        with open(OUTPUT_FILE, "a", newline="") as file:

            fields = [
                "timestamp",
                "pid",
                "name",
                "cpu_percent",
                "memory_percent",
                "io_read_bytes",
                "io_write_bytes",
                "voluntary_context_switches",
                "involuntary_context_switches",
                "num_threads",
                "status",
            ]

            writer = csv.DictWriter(
                file,
                fieldnames=fields
            )

            for process in psutil.process_iter():

                info = collect_process_info(process)

                if info:
                    writer.writerow(info)

        time.sleep(INTERVAL)


if __name__ == "__main__":
    monitor_processes()
