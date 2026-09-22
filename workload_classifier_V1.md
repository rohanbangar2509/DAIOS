(.daios_venv) rohan@ROHAN:~/DAIOS$ python ml/train_workload_classifier.py
Loading dataset...
Dataset shape: (76, 10)

Training samples: 57
Testing samples : 19

Training Random Forest...

==========================================
       DAIOS Workload Classifier
==========================================

Accuracy: 1.0000

Classification Report:
              precision    recall  f1-score   support

         cpu       1.00      1.00      1.00         6
          io       1.00      1.00      1.00         7
      memory       1.00      1.00      1.00         6

    accuracy                           1.00        19
   macro avg       1.00      1.00      1.00        19
weighted avg       1.00      1.00      1.00        19

Confusion Matrix:
[[6 0 0]
 [0 7 0]
 [0 0 6]]

Feature Importance:
                     feature  importance
1             memory_percent    0.270863
2                     rss_mb    0.254905
0                cpu_percent    0.177418
8                num_threads    0.158400
4        write_bytes_per_sec    0.076891
5   context_switches_per_sec    0.046604
3         read_bytes_per_sec    0.014919
6  minor_page_faults_per_sec    0.000000
7  major_page_faults_per_sec    0.000000

Model saved to:
ml/models/workload_classifier.pkl



However, don't call this a production-quality 100% classifier yet. Our dataset contains only 76 samples from three very controlled workloads, so the classes are extremely easy to separate.