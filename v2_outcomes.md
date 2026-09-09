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



## <b>Before Intentionally creating a CPU-bound workload</b>

<img width="1103" height="1016" alt="image" src="https://github.com/user-attachments/assets/9c998725-a14c-4492-90c8-885e33c09420" />

## <b>After Intentionally creating a CPU-bound workload</b>

<img width="948" height="633" alt="image" src="https://github.com/user-attachments/assets/fd36e048-37d4-413a-acf4-23d07f18d092" />
<img width="1078" height="1017" alt="image" src="https://github.com/user-attachments/assets/1536d4ad-e8c1-47b9-b558-c642e5910e8d" />

timestamp,pid,name,cpu_percent,memory_percent,io_read_bytes,io_write_bytes,voluntary_context_switches,involuntary_context_switches,num_threads,status
<img width="1171" height="512" alt="image" src="https://github.com/user-attachments/assets/23dc056b-3c42-43dd-a476-f8bd7a1c91b3" />


## <b>After Intentionally creating a I/O-bound workload</b>

<img width="1125" height="1087" alt="image" src="https://github.com/user-attachments/assets/c5405908-7d8d-41cd-be39-67830ab6c2dc" />

timestamp,pid,name,cpu_percent,memory_percent,io_read_bytes,io_write_bytes,voluntary_context_switches,involuntary_context_switches,num_threads,status
<img width="1258" height="505" alt="image" src="https://github.com/user-attachments/assets/c797e88a-be4a-4902-b2dd-bd22689a6d5f" />


## <b>After Intentionally creating a memory-bound workload</b>
<img width="1083" height="1087" alt="image" src="https://github.com/user-attachments/assets/db673a49-705c-4324-95c6-c45fdc019d6e" />

timestamp,pid,name,cpu_percent,memory_percent,io_read_bytes,io_write_bytes,voluntary_context_switches,involuntary_context_switches,num_threads,status
<img width="1140" height="508" alt="image" src="https://github.com/user-attachments/assets/c82f0b79-ca1d-46a9-a607-cc17fb25daad" />

