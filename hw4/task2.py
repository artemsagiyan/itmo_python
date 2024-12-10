import math
import concurrent.futures
import logging
import time
import os
import multiprocessing

logging.basicConfig(filename='integration_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(processName)s - %(message)s')

def integrate_parallel(f, a, b, *, n_jobs=1, n_iter=10000000, executor_type='thread'):
    step = (b - a) / n_iter
    if executor_type.lower() not in ['thread', 'process']:
        raise ValueError("executor_type must be 'thread' or 'process'")

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) if executor_type.lower() == 'thread' else concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = []
        for i in range(n_jobs):
            start = i * (n_iter // n_jobs)
            end = (i + 1) * (n_iter // n_jobs)
            if i == n_jobs -1:
                end = n_iter # handle the remainder for the last job

            future = executor.submit(partial_integration, f, a, b, start, end, step)
            futures.append(future)
            logging.info(f"Started job {i} from {start} to {end} using {executor_type}")

        acc = sum(future.result() for future in futures)
        return acc


def partial_integration(f, a, b, start, end, step):
    acc = 0
    for i in range(start, end):
        acc += f(a + i * step) * step
    return acc


if __name__ == "__main__":
    cpu_num = os.cpu_count()
    results = {}

    for executor_type in ['thread', 'process']:
        results[executor_type] = {}
        for n_jobs in range(1, cpu_num * 2 + 1):
            start_time = time.time()
            result = integrate_parallel(math.cos, 0, math.pi / 2, n_jobs=n_jobs, executor_type=executor_type)
            end_time = time.time()
            results[executor_type][n_jobs] = end_time - start_time
            print(f"Integration with {n_jobs} {executor_type} workers took {end_time - start_time:.4f} seconds. Result: {result}")

    with open('artifacts/results_task2.txt', 'w') as f:
        f.write("Execution time comparison:\n\n")
        for executor_type, data in results.items():
            f.write(f"{executor_type.capitalize()} Pool:\n")
            for n_jobs, time_taken in data.items():
                f.write(f"  {n_jobs} jobs: {time_taken:.4f} seconds\n")
            f.write("\n")

