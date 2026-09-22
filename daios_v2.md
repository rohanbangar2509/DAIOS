# DAIOS V2 — Outcomes & Validation

## 1. Overview

**DAIOS (Data-Aware Intelligence Operating System) V2** introduces an ML-based workload classification pipeline that monitors running processes and dynamically identifies their workload type based on system telemetry.

The current system supports three workload classes:

* **CPU**
* **IO**
* **MEMORY**

The workload classifier uses telemetry features such as:

* CPU utilization
* Memory utilization
* Resident Set Size (RSS)
* Disk write throughput
* Number of threads

The trained classifier is used by `predict_workload.py` to continuously monitor a process and infer its workload type in real time.

---

# 2. Project Structure

```text
DAIOS/
├── LICENSE
├── README.md
├── benchmarks/
├── daios_V2.md
├── dashboard/
├── docs/
│
├── ml/
│   ├── models/
│   │   └── workload_classifier.pkl
│   ├── predict_workload.py
│   ├── results/
│   └── train_workload_classifier.py
│
├── os/
├── streaming/
│
├── telemetry/
│   ├── process_monitor.py
│   ├── processed/
│   │   └── workload_dataset.csv
│   ├── raw/
│   │   ├── cpu_telemetry.csv
│   │   ├── io_telemetry.csv
│   │   └── memory_telemetry.csv
│   └── telemetry_processor.py
│
├── v1_outcomes.md
├── v2_outcomes.md
│
└── workloads/
    ├── cpu/
    │   └── cpu_workload.py
    │
    ├── io/
    │   ├── io_workload.py
    │   └── test_data.bin
    │
    └── memory/
        └── memory_workload.py
```

---

# 3. V2 ML Pipeline

The current V2 pipeline follows this workflow:

```text
Workload
   │
   ▼
Workload Generator
   │
   ├── CPU Workload
   ├── IO Workload
   └── Memory Workload
   │
   ▼
Process Telemetry
   │
   ▼
Raw Telemetry CSV
   │
   ▼
Telemetry Processor
   │
   ▼
Processed Workload Dataset
   │
   ▼
ML Training
   │
   ▼
Random Forest Classifier
   │
   ▼
workload_classifier.pkl
   │
   ▼
Real-Time Process Inference
   │
   ▼
CPU / IO / MEMORY
```

---

# 4. Workload Types

## 4.1 CPU Workload

The CPU workload is designed to generate sustained CPU utilization.

### Characteristics

Typical observed behavior:

| Feature          | Observed Value |
| ---------------- | -------------: |
| CPU Usage        |          ~100% |
| Memory Usage     |         ~0.12% |
| RSS              |        ~9.1 MB |
| Write Throughput |         0 MB/s |
| Threads          |              1 |
| Prediction       |            CPU |

The process consistently produces a CPU-intensive workload with minimal memory and disk activity.

---

## 4.2 IO Workload

The IO workload continuously performs disk write operations.

### Characteristics

Typical observed behavior:

| Feature          | Observed Range |
| ---------------- | -------------: |
| CPU Usage        |          ~3–9% |
| Memory Usage     |         ~0.13% |
| RSS              |       ~10.1 MB |
| Write Throughput |    ~9–133 MB/s |
| Threads          |              1 |
| Prediction       |             IO |

The defining characteristic of this workload is high disk write throughput combined with relatively low CPU and memory utilization.

---

## 4.3 Memory Workload

The memory workload allocates a large amount of memory and uses multiple threads.

### Characteristics

Typical observed behavior:

| Feature          | Observed Value |
| ---------------- | -------------: |
| CPU Usage        |          ~100% |
| Memory Usage     |        ~13.24% |
| RSS              |     ~1025.9 MB |
| Write Throughput |         0 MB/s |
| Threads          |             20 |
| Prediction       |         MEMORY |

The workload is clearly distinguished from the CPU workload through its significantly higher memory consumption and thread count.

---

# 5. ML Model

The trained workload classifier is stored at:

```text
ml/models/workload_classifier.pkl
```

The model is loaded by:

```text
ml/predict_workload.py
```

The inference pipeline extracts live process statistics and passes them to the trained classifier.

### Input Features

The classifier uses telemetry features including:

```text
CPU utilization
Memory utilization
RSS
Disk write throughput
Thread count
```

### Output

The classifier produces:

```text
Predicted workload class
Prediction confidence
```

Possible classes:

```text
CPU
IO
MEMORY
```

---

# 6. Real-Time Inference

The inference system can be executed using:

```bash
python ml/predict_workload.py <PID>
```

For example:

```bash
python ml/predict_workload.py 50822
```

The system first loads the trained classifier:

```text
Loading DAIOS workload classifier...
Model loaded successfully.
```

It then attaches to the specified process and continuously collects telemetry.

---

# 7. CPU Workload Inference

### Command

```bash
python ml/predict_workload.py 50822
```

### Target Process

```text
Process : python
Command : python workloads/cpu/cpu_workload.py
```

### Sample Inference

```text
[19:21:40] CPU=100.0% | MEM=0.12% | RSS=9.1 MB | WRITE=0.0 MB/s | THREADS=1 | PREDICTION=CPU | CONF=0.99

[19:21:42] CPU=100.2% | MEM=0.12% | RSS=9.1 MB | WRITE=0.0 MB/s | THREADS=1 | PREDICTION=CPU | CONF=1.00

[19:21:44] CPU=99.9% | MEM=0.12% | RSS=9.1 MB | WRITE=0.0 MB/s | THREADS=1 | PREDICTION=CPU | CONF=1.00

[19:21:47] CPU=99.9% | MEM=0.12% | RSS=9.1 MB | WRITE=0.0 MB/s | THREADS=1 | PREDICTION=CPU | CONF=1.00

[19:21:53] CPU=99.9% | MEM=0.12% | RSS=9.1 MB | WRITE=0.0 MB/s | THREADS=1 | PREDICTION=CPU | CONF=1.00
```

### Result

The classifier consistently identified the process as:

```text
CPU
```

with confidence values approximately between:

```text
0.99 – 1.00
```

This indicates stable classification for the CPU-intensive workload.

---

# 8. Invalid / Terminated Process Test

The inference system was also tested with a PID that no longer existed.

### Command

```bash
python ml/predict_workload.py 52771
```

### Result

```text
Loading DAIOS workload classifier...
Model loaded successfully.

Process 52771 does not exist.
```

This confirms that the inference script handles invalid or terminated PIDs without crashing.

---

# 9. IO Workload Inference

### Command

```bash
python ml/predict_workload.py 53056
```

### Target Process

```text
Process : python
Command : python workloads/io/io_workload.py
```

### Sample Inference

```text
[19:27:55] CPU=6.0% | MEM=0.13% | RSS=10.1 MB | WRITE=59.2 MB/s | THREADS=1 | PREDICTION=IO | CONF=1.00

[19:27:57] CPU=2.9% | MEM=0.13% | RSS=10.1 MB | WRITE=65.9 MB/s | THREADS=1 | PREDICTION=IO | CONF=1.00

[19:28:03] CPU=5.8% | MEM=0.13% | RSS=10.1 MB | WRITE=58.4 MB/s | THREADS=1 | PREDICTION=IO | CONF=1.00

[19:28:12] CPU=9.2% | MEM=0.13% | RSS=10.1 MB | WRITE=132.8 MB/s | THREADS=1 | PREDICTION=IO | CONF=1.00

[19:28:27] CPU=4.9% | MEM=0.13% | RSS=10.1 MB | WRITE=9.4 MB/s | THREADS=1 | PREDICTION=IO | CONF=0.87

[19:28:35] CPU=7.3% | MEM=0.13% | RSS=10.1 MB | WRITE=125.2 MB/s | THREADS=1 | PREDICTION=IO | CONF=1.00
```

### Result

The classifier consistently identified the process as:

```text
IO
```

Most predictions had:

```text
Confidence = 1.00
```

The lowest observed confidence was approximately:

```text
0.87
```

Even during lower write-throughput periods, the workload was still correctly classified as IO.

---

# 10. Memory Workload Inference

### Command

```bash
python ml/predict_workload.py 54181
```

### Target Process

```text
Process : python
Command : python workloads/memory/memory_workload.py
```

### Sample Inference

```text
[19:29:55] CPU=100.0% | MEM=13.24% | RSS=1025.9 MB | WRITE=0.0 MB/s | THREADS=20 | PREDICTION=MEMORY | CONF=1.00

[19:29:57] CPU=100.1% | MEM=13.24% | RSS=1025.9 MB | WRITE=0.0 MB/s | THREADS=20 | PREDICTION=MEMORY | CONF=1.00

[19:29:59] CPU=99.7% | MEM=13.24% | RSS=1025.9 MB | WRITE=0.0 MB/s | THREADS=20 | PREDICTION=MEMORY | CONF=0.99

[19:30:01] CPU=100.3% | MEM=13.24% | RSS=1025.9 MB | WRITE=0.0 MB/s | THREADS=20 | PREDICTION=MEMORY | CONF=0.98

[19:30:08] CPU=100.0% | MEM=13.24% | RSS=1025.9 MB | WRITE=0.0 MB/s | THREADS=20 | PREDICTION=MEMORY | CONF=0.99

[19:30:18] CPU=100.0% | MEM=13.24% | RSS=1025.9 MB | WRITE=0.0 MB/s | THREADS=20 | PREDICTION=MEMORY | CONF=0.99
```

### Result

The classifier consistently identified the process as:

```text
MEMORY
```

Observed confidence values were approximately:

```text
0.97 – 1.00
```

The model successfully distinguished the memory-intensive process from the CPU workload despite both workloads generating approximately 100% CPU utilization.

---

# 11. Validation Summary

| Workload |   CPU |  Memory |      RSS |  Write Rate | Threads | Prediction | Confidence |
| -------- | ----: | ------: | -------: | ----------: | ------: | ---------- | ---------: |
| CPU      | ~100% |  ~0.12% |    ~9 MB |      0 MB/s |       1 | **CPU**    |  0.99–1.00 |
| IO       | ~3–9% |  ~0.13% |   ~10 MB | ~9–133 MB/s |       1 | **IO**     |  0.87–1.00 |
| MEMORY   | ~100% | ~13.24% | ~1026 MB |      0 MB/s |      20 | **MEMORY** |  0.97–1.00 |

---

# 12. Key Observations

## CPU Workload

The CPU workload showed:

* Sustained ~100% CPU utilization.
* Very low memory utilization.
* Negligible disk write activity.
* Single-thread execution.
* Consistent `CPU` predictions.

The classifier maintained very high confidence throughout the observation period.

---

## IO Workload

The IO workload showed:

* Low-to-moderate CPU utilization.
* Very low memory utilization.
* High and variable disk write throughput.
* Single-thread execution.
* Consistent `IO` predictions.

Confidence decreased to approximately `0.87` during periods of relatively low write throughput, but the predicted class remained correct.

---

## Memory Workload

The memory workload showed:

* Approximately 100% CPU utilization.
* Significantly higher memory utilization.
* Approximately 1 GB RSS.
* No significant disk write activity.
* 20 active threads.
* Consistent `MEMORY` predictions.

An important observation is that CPU utilization alone is insufficient to distinguish CPU and memory workloads. Additional telemetry features such as RSS, memory utilization, and thread count provide useful separation.

---

# 13. V2 Validation Outcome

The DAIOS V2 workload inference pipeline successfully demonstrated real-time classification of the three implemented workload categories:

```text
CPU      → CPU
IO       → IO
MEMORY   → MEMORY
```

The classifier maintained high confidence across the tested workloads and successfully distinguished the CPU and memory workloads despite both producing approximately 100% CPU utilization.

The inference system also correctly handled a nonexistent process PID:

```text
Process <PID> does not exist.
```

Therefore, the current V2 implementation demonstrates the complete flow from:

```text
Workload Generation
        ↓
Telemetry Collection
        ↓
Telemetry Processing
        ↓
Dataset Creation
        ↓
ML Model Training
        ↓
Model Persistence
        ↓
Real-Time Process Monitoring
        ↓
Workload Classification
```

---

# 14. Current V2 Status

| Component             | Status        |
| --------------------- | ------------- |
| CPU Workload          | ✅ Implemented |
| IO Workload           | ✅ Implemented |
| Memory Workload       | ✅ Implemented |
| Process Telemetry     | ✅ Implemented |
| Raw Telemetry Storage | ✅ Implemented |
| Telemetry Processing  | ✅ Implemented |
| Workload Dataset      | ✅ Generated   |
| ML Classifier         | ✅ Trained     |
| Model Persistence     | ✅ Implemented |
| Real-Time Inference   | ✅ Implemented |
| CPU Classification    | ✅ Validated   |
| IO Classification     | ✅ Validated   |
| Memory Classification | ✅ Validated   |
| Invalid PID Handling  | ✅ Validated   |

---

# 15. Conclusion

DAIOS V2 has progressed from simple workload telemetry collection to an ML-driven workload intelligence layer.

The current implementation can observe a running process, extract its resource-usage characteristics, and classify the process into CPU, IO, or MEMORY workload categories in real time.

The validation results demonstrate that the trained classifier can identify the implemented synthetic workloads with consistently high confidence.

This establishes the foundation for the next stage of DAIOS: using workload classification to support intelligent operating-system-level decisions such as workload-aware resource management, scheduling, prioritization, and adaptive system optimization.
