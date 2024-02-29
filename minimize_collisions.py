from concurrent.futures import ProcessPoolExecutor, as_completed
from structs import table, hash_table
import math


def compute_best_bucket_size(range_start, range_end, word_list, page_size):
    bucket_size = 1
    collisions = math.inf
    for i in range(range_start, range_end):
        print(f"Computing bucket size {i}")
        # Assuming hash_table_instance can be created with these parameters
        # and has a method get_collisions() that works as expected.
        hash_table_instance = hash_table(table(word_list, page_size), i)
        current_collisions = hash_table_instance.get_collisions()
        if current_collisions < collisions:
            collisions = current_collisions
            bucket_size = i
    return bucket_size, collisions


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
    min_collisions = math.inf
    for future in as_completed(futures):
        bucket_size, collisions = future.result()
        if collisions < min_collisions:
            min_collisions = collisions
            best_bucket_size = bucket_size

    return best_bucket_size, min_collisions


if __name__ == "__main__":
    page_size = 1000

    file = open("words.txt", "r")
    word_list = file.readlines()
    word_list = [word.strip() for word in word_list]
    word_list = [word for word in word_list if len(word) > 0]

    best_bucket_size, min_collisions = parallel_compute_best_bucket(
        word_list, page_size
    )
    print(
        f"Best bucket size: {best_bucket_size} - Collisions: {min_collisions}"
    )  # Best bucket size: 905 - Collisions: 8405
