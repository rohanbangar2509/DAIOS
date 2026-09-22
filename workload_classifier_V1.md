# DAIOS Workload Classifier — Training Results

The DAIOS workload classifier was trained using telemetry data collected from three workload types:

* **CPU**
* **Memory**
* **I/O**

The classifier uses a **Random Forest** model to identify the type of workload based on process-level telemetry features.

---

## Dataset

| Metric            |         Value |
| ----------------- | ------------: |
| Total samples     |            76 |
| Training samples  |            57 |
| Testing samples   |            19 |
| Number of classes |             3 |
| Model             | Random Forest |

The dataset contains telemetry features such as CPU usage, memory usage, I/O rates, context switches, page faults, and thread count.

---

## Training

The model was trained using:

```bash
python ml/train_workload_classifier.py
```

Training output:

```text
Loading dataset...
Dataset shape: (76, 10)

Training samples: 57
Testing samples : 19

Training Random Forest...
```

---

## Model Performance

### Accuracy

```text
Accuracy: 1.0000
```

The model achieved **100% accuracy on the 19-sample test set**.

### Classification Report

```text
              precision    recall  f1-score   support

         cpu       1.00      1.00      1.00         6
          io       1.00      1.00      1.00         7
      memory       1.00      1.00      1.00         6

    accuracy                           1.00        19
   macro avg       1.00      1.00      1.00        19
weighted avg       1.00      1.00      1.00        19
```

All three workload classes achieved perfect precision, recall, and F1-score on the test set.

---

## Confusion Matrix

```text
[[6 0 0]
 [0 7 0]
 [0 0 6]]
```

| Actual \ Predicted | CPU | I/O | Memory |
| ------------------ | --: | --: | -----: |
| **CPU**            |   6 |   0 |      0 |
| **I/O**            |   0 |   7 |      0 |
| **Memory**         |   0 |   0 |      6 |

No misclassifications occurred in the current test set.

---

## Feature Importance

The Random Forest model reported the following feature importance values:

| Rank | Feature                     | Importance |
| ---: | --------------------------- | ---------: |
|    1 | `memory_percent`            |   0.270863 |
|    2 | `rss_mb`                    |   0.254905 |
|    3 | `cpu_percent`               |   0.177418 |
|    4 | `num_threads`               |   0.158400 |
|    5 | `write_bytes_per_sec`       |   0.076891 |
|    6 | `context_switches_per_sec`  |   0.046604 |
|    7 | `read_bytes_per_sec`        |   0.014919 |
|    8 | `minor_page_faults_per_sec` |   0.000000 |
|    9 | `major_page_faults_per_sec` |   0.000000 |

### Observations

The most influential features were:

* `memory_percent`
* `rss_mb`
* `cpu_percent`
* `num_threads`

This indicates that memory consumption, CPU utilization, and process characteristics currently provide the strongest separation between the workload classes.

I/O-related features such as `write_bytes_per_sec` and `read_bytes_per_sec` also contributed to classification, although their importance was lower in this dataset.

---

## Model Output

The trained model was successfully saved to:

```text
ml/models/workload_classifier.pkl
```

This model can be loaded later by the DAIOS workload classification pipeline for inference.

---

## Current Limitation

> **Important:** The current 100% accuracy should **not yet be considered production-level classifier performance**.

The dataset contains only **76 samples** collected from **three highly controlled workload types**. Because the workloads are intentionally designed to have distinct resource-usage patterns, the classes are relatively easy for the Random Forest model to separate.

Therefore, the current result demonstrates that the classification pipeline is functioning correctly, but it does **not yet establish that the model will generalize well to real-world workloads**.

---

## Next Steps

To make the classifier more robust, the dataset should be expanded with:

1. **More samples** for each workload type.
2. **Longer telemetry collection periods.**
3. **Different workload intensities**, such as low, medium, and high CPU usage.
4. **Mixed workloads**, such as CPU + I/O and CPU + Memory.
5. **Real-world applications and processes** rather than only synthetic workloads.
6. **Different process counts and thread counts.**
7. **Cross-validation** to obtain a more reliable estimate of model performance.
8. **A separate unseen evaluation dataset** collected independently from the training data.

A larger and more diverse dataset will help determine whether the classifier can generalize beyond the controlled workloads used during the initial experiment.

---

## Summary

The first version of the DAIOS workload classifier successfully demonstrates the complete ML pipeline:

```text
Telemetry Data
      ↓
Feature Extraction
      ↓
Workload Dataset
      ↓
Train/Test Split
      ↓
Random Forest
      ↓
Workload Classification
      ↓
Model Saved
```

The current experiment achieved:

```text
Dataset Size       : 76 samples
Training Samples   : 57
Testing Samples    : 19
Classes            : CPU / I/O / Memory
Model              : Random Forest
Test Accuracy      : 100%
Model Status       : Successfully trained and saved
```

The result is a **successful initial proof of concept**, while additional data and more realistic workloads are required before evaluating the classifier for production use.
