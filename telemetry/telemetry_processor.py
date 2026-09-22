import pandas as pd
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

RAW_DIR = Path("telemetry/raw")

OUTPUT_FILE = Path(
    "telemetry/processed/workload_dataset.csv"
)


# ============================================================
# Load telemetry files
# ============================================================

files = [
    RAW_DIR / "cpu_telemetry.csv",
    RAW_DIR / "io_telemetry.csv",
    RAW_DIR / "memory_telemetry.csv",
]


dataframes = []


for file in files:

    print(f"Loading: {file}")

    df = pd.read_csv(file)

    dataframes.append(df)


# ============================================================
# Combine datasets
# ============================================================

df = pd.concat(
    dataframes,
    ignore_index=True
)


print()
print("Combined dataset:")
print(df.shape)


# ============================================================
# Keep only actual workloads
# ============================================================

workload_mask = (
    df["cmdline"].str.contains(
        "workloads/",
        na=False
    )
)

df = df[workload_mask].copy()


# ============================================================
# Remove first sample of each process
# ============================================================

# The first sample has zero CPU/I/O/rate values because
# there is no previous observation available.

df = df[
    ~(
        (df["cpu_percent"] == 0) &
        (df["read_bytes_per_sec"] == 0) &
        (df["write_bytes_per_sec"] == 0) &
        (df["context_switches_per_sec"] == 0)
    )
].copy()


# ============================================================
# Select ML features
# ============================================================

features = [

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


target = "workload_type"


dataset = df[
    features + [target]
].copy()


# ============================================================
# Clean numerical values
# ============================================================

dataset = dataset.replace(
    [float("inf"), float("-inf")],
    pd.NA
)

dataset = dataset.dropna()


# ============================================================
# Save dataset
# ============================================================

dataset.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# Display results
# ============================================================

print()
print("==========================================")
print("      DAIOS ML Dataset Created")
print("==========================================")

print()

print("Dataset shape:")
print(dataset.shape)

print()

print("Class distribution:")
print(
    dataset["workload_type"].value_counts()
)

print()

print("Dataset preview:")
print(
    dataset.head(10)
)

print()

print(f"Saved to: {OUTPUT_FILE}")
