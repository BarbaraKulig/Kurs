import multiprocessing


def factorize_single(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors


def factorize(numbers):
    result = []
    for number in numbers:
        result.append(factorize_single(number))
    return result


def factorize_parallel(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors


def factorize_parallel_wrapper(numbers):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        return pool.map(factorize_parallel, numbers)


if __name__ == "__main__":
    # Test the synchronous version
    result_sync = factorize([128, 255, 99999, 10651060])

    # Measure the execution time of the synchronous version
    import time

    start_time = time.time()
    factorize([128, 255, 99999, 10651060])
    sync_execution_time = time.time() - start_time
    print(f"Synchronous execution time: {sync_execution_time} seconds")

    # Test the parallel version
    result_parallel = factorize_parallel_wrapper([128, 255, 99999, 10651060])

    # Measure the execution time of the parallel version
    start_time = time.time()
    factorize_parallel_wrapper([128, 255, 99999, 10651060])
    parallel_execution_time = time.time() - start_time
    print(f"Parallel execution time: {parallel_execution_time} seconds")

    # Verify that the results are the same for both versions
    assert result_sync == result_parallel
