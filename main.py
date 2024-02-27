import tkinter as tk
from tkinter import scrolledtext
from structs import table, hash_table
import time


class WordSearchGUI:
    def __init__(self, master):
        self.master = master
        master.title("Word Search")

        self.label_word = tk.Label(master, text="Word:")
        self.label_word.pack()

        self.entry_word = tk.Entry(master)
        self.entry_word.pack()
        self.entry_word.insert(0, "hello")  # Default value for word

        self.label_page_size = tk.Label(master, text="Page Size:")
        self.label_page_size.pack()

        self.entry_page_size = tk.Entry(master)
        self.entry_page_size.pack()
        self.entry_page_size.insert(0, "1000")  # Default value for page_size

        self.label_bucket_size = tk.Label(master, text="Bucket Size:")
        self.label_bucket_size.pack()

        self.entry_bucket_size = tk.Entry(master)
        self.entry_bucket_size.pack()
        self.entry_bucket_size.insert(0, "100")  # Default value for bucket_size

        self.generate_table_button = tk.Button(
            master,
            text="Generate Table Structures",
            command=self.generate_table_structures,
        )
        self.generate_table_button.pack()

        self.search_button = tk.Button(master, text="Search", command=self.find_word)
        self.search_button.pack()
        self.search_button["state"] = "disabled"  # Initially disable the search button

        self.result_area = scrolledtext.ScrolledText(master, height=10)
        self.result_area.pack()

        self.table_instance = None
        self.hash_table_instance = None

    def generate_table_structures(self):
        page_size = int(self.entry_page_size.get())
        bucket_size = int(self.entry_bucket_size.get())

        file = open("words.txt", "r")
        word_list = file.readlines()
        word_list = [word.strip() for word in word_list]
        word_list = [word for word in word_list if len(word) > 0]

        self.table_instance = table(word_list, page_size)
        self.hash_table_instance = hash_table(self.table_instance, bucket_size)

        self.result_area.insert(
            tk.END,
            f"Table and Hash Table structures have been generated with page size {page_size} and bucket size {bucket_size}\n",
        )
        self.result_area.insert(
            tk.END, f"Collisions: {self.hash_table_instance.get_collisions()}\n"
        )
        self.result_area.insert(
            tk.END, f"Overflows: {self.hash_table_instance.get_overflows()}\n"
        )
        self.search_button["state"] = (
            "normal"  # Enable the search button after structures are generated
        )

    def find_word(self):
        self.result_area.delete("1.0", tk.END)
        word = self.entry_word.get()

        if self.table_instance is None or self.hash_table_instance is None:
            self.result_area.insert(
                tk.END, "Please generate table structures before searching.\n"
            )
            return

        [result, time_elapsed, memory_access_count] = self.table_scan_word(
            self.table_instance, word
        )
        if result is None:
            self.result_area.insert(
                tk.END, f"Table scan not found, time: {time_elapsed:.5f}.\n"
            )
        else:
            self.result_area.insert(
                tk.END,
                f"Table scan found {result.get_value()} at index {result.get_index()}, time: {time_elapsed:.5f}, memory_access_count: {memory_access_count}\n",
            )

        [result, time_elapsed, memory_access_count] = (
            self.hash_table_instance.get_word_tuple(word)
        )
        if result is None:
            self.result_area.insert(
                tk.END,
                f"Hash table not found, time: {time_elapsed:.5f}, memory_access_count: {memory_access_count}\n",
            )
        else:
            self.result_area.insert(
                tk.END,
                f"Hash table found {result.get_value()} at index {result.get_index()}, time: {time_elapsed:.5f}, memory_access_count: {memory_access_count}\n",
            )

    def table_scan_word(self, table_instance, word):
        memory_access_count = 0
        start_time = time.time()
        for page in table_instance._pages:
            memory_access_count += 1
            for tuple in page.get_page():
                if tuple.get_value() == word:
                    return [tuple, time.time() - start_time, memory_access_count]

        return [None, time.time() - start_time, memory_access_count]


if __name__ == "__main__":
    root = tk.Tk()
    gui = WordSearchGUI(root)
    root.mainloop()
