import time
import threading
import multiprocessing
import os

def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def run_fibonacci(n, method, results):
    start_time = time.time()
    result = fibonacci(n)
    end_time = time.time()
    results.append((method, end_time - start_time))

def main():
    n = 100000
    iterations = 10

    # Synchronous execution
    sync_results = []
    start_time = time.time()
    for i in range(iterations):
        run_fibonacci(n, "sync", sync_results)
    end_time = time.time()
    sync_total_time = end_time - start_time

    # Threading
    thread_results = []
    threads = []
    start_time = time.time()
    for i in range(iterations):
        thread = threading.Thread(target=run_fibonacci, args=(n, "thread", thread_results))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end_time = time.time()
    thread_total_time = end_time - start_time


    # Multiprocessing
    process_results = []
    processes = []
    start_time = time.time()
    for i in range(iterations):
        process = multiprocessing.Process(target=run_fibonacci, args=(n, "process", process_results))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    end_time = time.time()
    process_total_time = end_time - start_time

    with open("artifacts/results_task1.txt", "w") as f:
        f.write(f"Synchronous execution: {sync_total_time:.4f} seconds\n")
        f.write(f"Threading: {thread_total_time:.4f} seconds\n")
        f.write(f"Multiprocessing: {process_total_time:.4f} seconds\n")

if __name__ == "__main__":
    main()
