import psutil
import csv
import time
import os
import sys
from datetime import datetime


# ============================================================
# Configuration
# ============================================================

INTERVAL = 2

# Workload label passed from command line
# Example:
# python telemetry/process_monitor.py cpu
# python telemetry/process_monitor.py io
# python telemetry/process_monitor.py memory

WORKLOAD_TYPE = sys.argv[1] if len(sys.argv) > 1 else "unknown"

OUTPUT_FILE = f"telemetry/raw/{WORKLOAD_TYPE}_telemetry.csv"

# Store previous cumulative counters
previous_stats = {}

# PID of this telemetry collector
CURRENT_PID = os.getpid()


# ============================================================
# Process Information
# ============================================================

def get_process_info(process):

    try:

        with process.oneshot():

            pid = process.pid

            # ------------------------------------------------
            # Command line
            # ------------------------------------------------

            try:
                cmdline = " ".join(process.cmdline())
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                cmdline = ""

            # ------------------------------------------------
            # Ignore telemetry collector itself
            # ------------------------------------------------

            if pid == CURRENT_PID:
                return None

            # ------------------------------------------------
            # CPU / Memory
            # ------------------------------------------------

            cpu_percent = process.cpu_percent(None)

            memory_percent = process.memory_percent()

            memory_info = process.memory_info()

            rss_mb = memory_info.rss / (1024 * 1024)

            # ------------------------------------------------
            # I/O counters
            # ------------------------------------------------

            try:

                io = process.io_counters()

                read_bytes = io.read_bytes
                write_bytes = io.write_bytes

            except (
                psutil.AccessDenied,
                psutil.NoSuchProcess
            ):

                read_bytes = 0
                write_bytes = 0

            # ------------------------------------------------
            # Context switches
            # ------------------------------------------------

            try:

                ctx = process.num_ctx_switches()

                voluntary = ctx.voluntary
                involuntary = ctx.involuntary

            except (
                psutil.AccessDenied,
                psutil.NoSuchProcess
            ):

                voluntary = 0
                involuntary = 0

            # ------------------------------------------------
            # Page faults
            # Linux /proc/<pid>/stat
            # ------------------------------------------------

            minor_faults = 0
            major_faults = 0

            try:

                with open(f"/proc/{pid}/stat", "r") as stat_file:

                    stat_data = stat_file.read()

                # The process name is inside parentheses and can
                # theoretically contain spaces.
                # Therefore, split only after the final ')'.

                closing_paren = stat_data.rfind(")")

                stat_rest = stat_data[closing_paren + 2:].split()

                # stat_rest index mapping:
                #
                # index 0  = state (field 3)
                # index 7  = minor faults (field 10)
                # index 9  = major faults (field 12)

                minor_faults = int(stat_rest[7])

                major_faults = int(stat_rest[9])

            except (
                FileNotFoundError,
                PermissionError,
                IndexError,
                ValueError
            ):

                minor_faults = 0
                major_faults = 0

            # ------------------------------------------------
            # Other process information
            # ------------------------------------------------

            num_threads = process.num_threads()

            status = process.status()

            now = time.time()

            # ------------------------------------------------
            # Rates
            # ------------------------------------------------

            read_rate = 0
            write_rate = 0

            context_switch_rate = 0

            minor_fault_rate = 0
            major_fault_rate = 0

            # ------------------------------------------------
            # Calculate rates from previous sample
            # ------------------------------------------------

            if pid in previous_stats:

                previous = previous_stats[pid]

                elapsed = now - previous["timestamp"]

                if elapsed > 0:

                    # ------------------------------
                    # I/O
                    # ------------------------------

                    read_delta = (
                        read_bytes -
                        previous["read_bytes"]
                    )

                    write_delta = (
                        write_bytes -
                        previous["write_bytes"]
                    )

                    if read_delta >= 0:

                        read_rate = (
                            read_delta / elapsed
                        )

                    if write_delta >= 0:

                        write_rate = (
                            write_delta / elapsed
                        )

                    # ------------------------------
                    # Context switches
                    # ------------------------------

                    voluntary_delta = (
                        voluntary -
                        previous["voluntary"]
                    )

                    involuntary_delta = (
                        involuntary -
                        previous["involuntary"]
                    )

                    total_context_delta = (
                        voluntary_delta +
                        involuntary_delta
                    )

                    if total_context_delta >= 0:

                        context_switch_rate = (
                            total_context_delta /
                            elapsed
                        )

                    # ------------------------------
                    # Page faults
                    # ------------------------------

                    minor_delta = (
                        minor_faults -
                        previous["minor_faults"]
                    )

                    major_delta = (
                        major_faults -
                        previous["major_faults"]
                    )

                    if minor_delta >= 0:

                        minor_fault_rate = (
                            minor_delta / elapsed
                        )

                    if major_delta >= 0:

                        major_fault_rate = (
                            major_delta / elapsed
                        )

            # ------------------------------------------------
            # Store current cumulative counters
            # ------------------------------------------------

            previous_stats[pid] = {

                "timestamp": now,

                "read_bytes": read_bytes,

                "write_bytes": write_bytes,

                "voluntary": voluntary,

                "involuntary": involuntary,

                "minor_faults": minor_faults,

                "major_faults": major_faults,
            }

            # ------------------------------------------------
            # Return telemetry row
            # ------------------------------------------------

            return [

                datetime.now().isoformat(
                    timespec="seconds"
                ),

                pid,

                process.ppid(),

                process.name(),

                cmdline,

                round(cpu_percent, 2),

                round(memory_percent, 4),

                round(rss_mb, 2),

                round(read_rate, 2),

                round(write_rate, 2),

                round(context_switch_rate, 2),

                round(minor_fault_rate, 2),

                round(major_fault_rate, 2),

                num_threads,

                status,

                WORKLOAD_TYPE
            ]

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess
    ):

        return None


# ============================================================
# Main Telemetry Collector
# ============================================================

def main():

    print("==========================================")
    print("       DAIOS Telemetry Collector")
    print("==========================================")

    print(f"Workload type : {WORKLOAD_TYPE}")
    print(f"Output file   : {OUTPUT_FILE}")
    print(f"Interval      : {INTERVAL} seconds")
    print("Press Ctrl+C to stop.")
    print()

    # --------------------------------------------------------
    # Create / reset CSV
    # --------------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            "timestamp",

            "pid",

            "ppid",

            "name",

            "cmdline",

            "cpu_percent",

            "memory_percent",

            "rss_mb",

            "read_bytes_per_sec",

            "write_bytes_per_sec",

            "context_switches_per_sec",

            "minor_page_faults_per_sec",

            "major_page_faults_per_sec",

            "num_threads",

            "status",

            "workload_type"
        ])

    # --------------------------------------------------------
    # Collection loop
    # --------------------------------------------------------

    try:

        while True:

            rows = []

            for process in psutil.process_iter():

                data = get_process_info(process)

                if data is not None:

                    rows.append(data)

            # ------------------------------------------------
            # Append collected rows
            # ------------------------------------------------

            with open(
                OUTPUT_FILE,
                "a",
                newline=""
            ) as file:

                writer = csv.writer(file)

                writer.writerows(rows)

            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] "
                f"Collected {len(rows)} processes"
            )

            time.sleep(INTERVAL)

    except KeyboardInterrupt:

        print()
        print("Telemetry collector stopped.")


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":

    main()