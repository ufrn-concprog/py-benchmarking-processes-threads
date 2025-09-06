# Benchmarking Processes and Threads in Python

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/3)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Build](https://img.shields.io/badge/build-manual-lightgrey)

This benchmark measures the overhead of creating processes, child processes, and threads in Python. The goal is to demonstrate that creating threads is far more efficient than creating processes.

This project is part of the **Concurrent Programming** module at the [Federal University of Rio Grande do Norte (UFRN)](https://www.ufrn.br), Natal, Brazil.

## 📃 Description

This benchmark measures the time to create 1,000 processes, child processes, and threads. This number is currently fixed and hard-coded, but it can be adjusted and even provided as a user input to the program. All the working units execute the very same task, which does almost nothing to allow for focusing on the overhead. For the case of child processes, a parent process is created, and then it creates multiple child processes.

The benchmark currently runs for only one. Future work involves modifying the implementation to support multiple runs (at least 20) for empirical validity, and recording the mean and standard deviation.

---

## 📂 Repository Structure

```
.
├── src/                # Source code
│   ├── benchmark.py    # Benchmark implementation
└── README.md
```

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3+
- A terminal or IDE

### ▶️ Running

```bash
python3 benchmark
```

Expected output:

```
Processes       | 4.5978 seconds for 1000 processes
Child Processes | 4.4675 seconds for 1000 child processes
Threads         | 0.0313 seconds for 1000 threads
```

The expected result is that creating multiple threads is far more efficient than creating processes.

---

## 📝 Important Things to Note

Although the implementation of this benchmark is portable across mainstream platforms (Windows, Linux, macOS), there are some differences in how they handle the creation of processes that can interfere with both implementation and execution.

For the Python implementation on Windows and macOS operating systems, the multiprocessing start method is *spawn*. With 'spawn', Python needs to pickle the function to send it to the child process, and local (nested) functions cannot be pickled. On Linux, the default start method is *fork*, so this issue does not occur there because the child process inherits the parent process's memory space, allowing it to call even local functions. Although it is possible to force the use of *fork* on macOS with `multiprocessing.set_start_method("fork")`, this approach does not work on Windows and breaks the program's portability.

In some cases, creating child processes may be slower than creating processes directly. This is also a consequence of using *spawn* on Windows and macOS operating systems. Every new process starts a fresh Python interpreter and must import the module, pickle arguments, and initialize the state. For child processes, one parent process is spawned from the primary Python interpreter, plus *n* child processes spawned from the parent. This means that the system effectively does two layers of spawn overhead: first for the parent process, then for each child process, thus slowing down performance. On Linux with *fork*, the overhead would be less noticeable because child processes inherit the memory image.

---

## 🤝 Contributing

Contributions are welcome! Fork this repository and submit a pull request 🚀

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
