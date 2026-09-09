## v2 Architecture

                    DAIOS Workloads
                          │
            ┌─────────────┼─────────────┐
            ↓             ↓             ↓
       CPU-bound       I/O-bound    Memory-bound
            │             │             │
            ↓             ↓             ↓
       High CPU        High Disk     High RAM
            │             │             │
            └─────────────┼─────────────┘
                          ↓
                    Telemetry
                          ↓
                     ML Dataset



<b>Before Intentionally creating a CPU-bound workload</b>

<img width="1103" height="1016" alt="image" src="https://github.com/user-attachments/assets/9c998725-a14c-4492-90c8-885e33c09420" />

<b>After Intentionally creating a CPU-bound workload</b>

<img width="948" height="633" alt="image" src="https://github.com/user-attachments/assets/fd36e048-37d4-413a-acf4-23d07f18d092" />
<img width="1078" height="1017" alt="image" src="https://github.com/user-attachments/assets/1536d4ad-e8c1-47b9-b558-c642e5910e8d" />

<b>After Intentionally creating a I/O-bound workload</b>

<img width="1125" height="1087" alt="image" src="https://github.com/user-attachments/assets/c5405908-7d8d-41cd-be39-67830ab6c2dc" />

<b>After Intentionally creating a memory-bound workload</b>
<img width="1083" height="1087" alt="image" src="https://github.com/user-attachments/assets/db673a49-705c-4324-95c6-c45fdc019d6e" />
