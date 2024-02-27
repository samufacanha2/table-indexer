from structs import *
import time


def table_scan_word(table_instance: table, word: str):
    # count the execution time of the function
    memory_access_count = 0
    start_time = time.time()
    for page in table_instance._pages:
        memory_access_count += 1
        for tuple in page.get_page():
            if tuple.get_value() == word:
                return [tuple, time.time() - start_time, memory_access_count]

    return [None, time.time() - start_time, memory_access_count]


def find_word(word: str, page_size: int, bucket_size: int):
    file = open("words.txt", "r")

    word_list = file.readlines()
    word_list = [word.strip() for word in word_list]
    word_list = [word for word in word_list if len(word) > 0]

    table_instance = table(word_list, page_size)
    hash_table_instance = hash_table(table_instance, bucket_size)

    [result, time, memory_access_count] = table_scan_word(table_instance, word)
    if result is None:
        print(f"not found, time: {time}")

    if type(result) is tuple:
        print(
            f"found {result.get_value()} at index {result.get_index()}, time: {time}, memory_access_count: {memory_access_count}"
        )

    [result, time, memory_access_count] = hash_table_instance.get_word_tuple(word)
    if result is None:
        print(f"not found, time: {time}, memory_access_count: {memory_access_count}")

    if type(result) is tuple:
        print(
            f"found {result.get_value()} at index {result.get_index()}, time: {time}, memory_access_count: {memory_access_count}"
        )


PAGE_SIZE = 1000
BUCKET_SIZE = 100
find_word("hello", PAGE_SIZE, BUCKET_SIZE)
