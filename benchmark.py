import time
from threading import Thread
from multiprocessing import Process

# Task function to run by both processes and threads
def do_task():
    """
    A simple task that does almost nothing.
    It is intentionally trivial to measure mostly the overhead of
    creating and managing processes/threads rather than doing work.
    """
    return

# Parent task for child processes
def parent_task(count):
    """
    A parent process that spawns `count` child processes, each one running 'do_task'.

    NOTE: This must be a *top-level function* (not nested inside another)
    because the multiprocessing start method is 'spawn' on macOS and Windows
    operating systems. Python needs to pickle the function to send it to the child
    process, and local (nested) functions cannot be pickled.
    """
    workers = []
    for _ in range(count):
        p = Process(target=do_task)
        workers.append(p)
        p.start()

    for p in workers:
        p.join()

# Benchmark function
def benchmark(label, creator, numworkers, use_parent=False):
    """
    Benchmark the time it takes to create and join workers.

    Parameters:
        label     : str  - Label for the benchmark
        creator   : func - Thread/Process constructor or callable
        numworkers: int  - Number of work units (processes, threads) to create
        use_parent: bool - If True, run a parent process that spawns child processes
    """
    start_time = time.perf_counter()

    if use_parent:
        # Launch one parent process that will spawn child processes
        worker = Process(target=parent_task, args=(numworkers,))
        worker.start()
        worker.join()

    else:
        # Regular threads or processes
        workers = []
        for _ in range(numworkers):
            worker = creator(target=do_task)
            workers.append(worker)
            worker.start()

        for worker in workers:
            worker.join()

    end_time = time.perf_counter()
    print(f"{label.ljust(16)}| {end_time - start_time:.4f} seconds for {numworkers} {label.lower()}")

# Main driver
def main():
    numworkers = 1000     # Number of work units to create

    print("Benchmarking creation of processes vs threads:\n")

    # Benchmark processes
    benchmark("Processes", Process, numworkers)

    # Benchmark child processes (via parent process)
    benchmark("Child Processes", Process, numworkers, use_parent=True)

    # Benchmark threads
    benchmark("Threads", Thread, numworkers)

if __name__ == "__main__":
    # On macOS and Windows operating systems, the default start method is 'spawn'.
    # On Linux, the default is 'fork'. For portability, rely on 'spawn'.
    # If desired, it possible to force 'fork' on macOS with:
    # multiprocessing.set_start_method("fork")
    main()