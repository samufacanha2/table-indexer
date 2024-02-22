from structs import *
import time


def table_scan_word(table_instance: table, word: str):
    # count the execution time of the function
    start_time = time.time()
    for page in table_instance._pages:
        for tuple in page:
            if tuple.get_value() == word:
                return [tuple, time.time() - start_time]

    return [None, time.time() - start_time]


file = open("words.txt", "r")

word_list = file.readlines()
word_list = [word.strip() for word in word_list]
word_list = [word for word in word_list if len(word) > 0]

table_instance = table(word_list)  # table created

[result, time] = table_scan_word(table_instance, "hello")
if result is None:
    print(f"not found, time: {time}")

if type(result) is tuple:
    print(f"found at index {result.get_value()}, time: {time}")

indexed_table_instance = indexed_table(table_instance)

[result, time] = indexed_table_instance.find_word("hello")
if result is None:
    print(f"not found, time: {time}")

if type(result) is tuple:
    print(f"found at index {result.get_value()}, time: {time}")
