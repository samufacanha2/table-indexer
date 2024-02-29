from concurrent.futures import ProcessPoolExecutor, as_completed
from structs import table, hash_table
import math


def compute_best_bucket_size(range_start, range_end, word_list, page_size):
    bucket_size = 1
    overflows = math.inf
    for i in range(range_start, range_end):
        print(f"Computing bucket size {i}")
        # Assuming hash_table_instance can be created with these parameters
        # and has a method get_overflows() that works as expected.
        hash_table_instance = hash_table(table(word_list, page_size), i)
        current_overflows = hash_table_instance.get_overflows()
        if current_overflows < overflows:
            overflows = current_overflows
            bucket_size = i
    return bucket_size, overflows


def parallel_compute_best_bucket(word_list, page_size, workers=10):
    total_range = 1000
    step = total_range // workers
    futures = []
    with ProcessPoolExecutor(max_workers=workers) as executor:
        for i in range(0, workers):
            range_start = i * step + 1
            range_end = (i + 1) * step if i < workers - 1 else total_range
            futures.append(
                executor.submit(
                    compute_best_bucket_size,
                    range_start,
                    range_end,
                    word_list,
                    page_size,
                )
            )

    best_bucket_size = 1
    min_overflows = math.inf
    for future in as_completed(futures):
        bucket_size, overflows = future.result()
        if overflows < min_overflows:
            min_overflows = overflows
            best_bucket_size = bucket_size

    return best_bucket_size, min_overflows


if __name__ == "__main__":
    page_size = 1000

    file = open("words.txt", "r")
    word_list = file.readlines()
    word_list = [word.strip() for word in word_list]
    word_list = [word for word in word_list if len(word) > 0]

    best_bucket_size, min_overflows = parallel_compute_best_bucket(word_list, page_size)
    print(f"Best bucket size: {best_bucket_size} - Overflows: {min_overflows}")
    # Best bucket size: 913 - Overflows: 1 (minimizing overflows)
