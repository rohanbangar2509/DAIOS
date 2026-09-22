import sys
import time
import joblib
import psutil
import pandas as pd


# ============================================================
# Configuration
# ============================================================

MODEL_PATH = "ml/models/workload_classifier.pkl"

INTERVAL = 2


FEATURES = [
    "cpu_percent",
    "memory_percent",
    "rss_mb",
    "read_bytes_per_sec",
    "write_bytes_per_sec",
    "context_switches_per_sec",
    "minor_page_faults_per_sec",
    "major_page_faults_per_sec",
    "num_threads",
]


# ============================================================
# Load model
# ============================================================

print("Loading DAIOS workload classifier...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully.")


# ============================================================
# PID
# ============================================================

if len(sys.argv) < 2:

    print()
    print("Usage:")
    print(
        "python ml/predict_workload.py <PID>"
    )
    print()

    sys.exit(1)


PID = int(sys.argv[1])


# ============================================================
# Process
# ============================================================

try:

    process = psutil.Process(PID)

except psutil.NoSuchProcess:

    print(f"Process {PID} does not exist.")

    sys.exit(1)


print()
print("==========================================")
print("        DAIOS Workload Inference")
print("==========================================")

print(f"PID     : {PID}")
print(f"Process : {process.name()}")

try:

    print(
        f"Command : {' '.join(process.cmdline())}"
    )

except Exception:

    pass

print()


# ============================================================
# Prime CPU measurement
# ============================================================

process.cpu_percent(None)


# ============================================================
# Previous counters
# ============================================================

previous_time = time.time()

try:

    io = process.io_counters()

    previous_read = io.read_bytes
    previous_write = io.write_bytes

except Exception:

    previous_read = 0
    previous_write = 0


try:

    ctx = process.num_ctx_switches()

    previous_context = (
        ctx.voluntary +
        ctx.involuntary
    )

except Exception:

    previous_context = 0


# ============================================================
# Main inference loop
# ============================================================

while True:

    try:

        time.sleep(INTERVAL)

        # ----------------------------------------------------
        # CPU
        # ----------------------------------------------------

        cpu_percent = process.cpu_percent(None)

        # ----------------------------------------------------
        # Memory
        # ----------------------------------------------------

        memory_percent = process.memory_percent()

        memory_info = process.memory_info()

        rss_mb = (
            memory_info.rss /
            (1024 * 1024)
        )

        # ----------------------------------------------------
        # I/O
        # ----------------------------------------------------

        try:

            io = process.io_counters()

            current_read = io.read_bytes
            current_write = io.write_bytes

        except Exception:

            current_read = previous_read
            current_write = previous_write

        # ----------------------------------------------------
        # Context switches
        # ----------------------------------------------------

        try:

            ctx = process.num_ctx_switches()

            current_context = (
                ctx.voluntary +
                ctx.involuntary
            )

        except Exception:

            current_context = previous_context

        # ----------------------------------------------------
        # Time
        # ----------------------------------------------------

        current_time = time.time()

        elapsed = current_time - previous_time

        if elapsed <= 0:

            elapsed = INTERVAL

        # ----------------------------------------------------
        # Rates
        # ----------------------------------------------------

        read_rate = max(
            0,
            (current_read - previous_read)
            / elapsed
        )

        write_rate = max(
            0,
            (current_write - previous_write)
            / elapsed
        )

        context_switch_rate = max(
            0,
            (current_context - previous_context)
            / elapsed
        )

        # ----------------------------------------------------
        # Page faults
        # ----------------------------------------------------

        minor_fault_rate = 0
        major_fault_rate = 0

        try:

            with open(
                f"/proc/{PID}/stat",
                "r"
            ) as file:

                stat_data = file.read()

            closing_paren = stat_data.rfind(")")

            stat_rest = (
                stat_data[
                    closing_paren + 2:
                ].split()
            )

            minor_faults = int(
                stat_rest[7]
            )

            major_faults = int(
                stat_rest[9]
            )

        except Exception:

            minor_faults = 0
            major_faults = 0

        # ----------------------------------------------------
        # Threads
        # ----------------------------------------------------

        num_threads = process.num_threads()

        # ----------------------------------------------------
        # Create feature vector
        # ----------------------------------------------------

        features = pd.DataFrame(
            [[
                cpu_percent,
                memory_percent,
                rss_mb,
                read_rate,
                write_rate,
                context_switch_rate,
                minor_fault_rate,
                major_fault_rate,
                num_threads,
            ]],
            columns=FEATURES
        )

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        prediction = model.predict(
            features
        )[0]

        probabilities = model.predict_proba(
            features
        )[0]

        confidence = probabilities.max()

        # ----------------------------------------------------
        # Output
        # ----------------------------------------------------

        print(
            f"[{time.strftime('%H:%M:%S')}] "
            f"CPU={cpu_percent:6.1f}% | "
            f"MEM={memory_percent:6.2f}% | "
            f"RSS={rss_mb:8.1f} MB | "
            f"WRITE={write_rate / (1024 * 1024):8.1f} MB/s | "
            f"THREADS={num_threads:2d} | "
            f"PREDICTION={prediction.upper():7s} | "
            f"CONF={confidence:.2f}"
        )

        # ----------------------------------------------------
        # Update previous counters
        # ----------------------------------------------------

        previous_read = current_read
        previous_write = current_write
        previous_context = current_context
        previous_time = current_time

    except KeyboardInterrupt:

        print()
        print("Inference stopped.")

        break

    except psutil.NoSuchProcess:

        print()
        print("Process ended.")

        break
