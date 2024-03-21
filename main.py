import tkinter as tk
from tkinter import scrolledtext
from structs import table, hash_table
import time


class WordSearchGUI:

    def __init__(self, master):
        self.master = master
        master.title("Word Search")

        row = 0

        # head
        self.label_head = tk.Label(master, text="Head Lines:")
        self.label_head.grid(row=row, column=0, sticky="e")

        self.head_size = tk.Entry(master)
        self.head_size.grid(row=row, column=1)
        self.head_size.insert(0, "5")

        self.head_button = tk.Button(master, text="Head", command=self.head)
        self.head_button.grid(row=row, column=2, sticky="w")
        self.head_button["state"] = "disabled"

        row += 1

        # Input Section
        self.label_word = tk.Label(master, text="Word:")
        self.label_word.grid(row=row, column=0, sticky="e")

        self.entry_word = tk.Entry(master)
        self.entry_word.grid(row=row, column=1)
        self.entry_word.insert(0, "hello")

        self.search_button = tk.Button(master, text="Search", command=self.find_word)
        self.search_button.grid(row=row, column=2, sticky="w")
        self.search_button["state"] = "disabled"

        row += 1

        self.label_page_size = tk.Label(master, text="Page Size:")
        self.label_page_size.grid(row=row, column=0, sticky="e")

        self.entry_page_size = tk.Entry(master)
        self.entry_page_size.grid(row=row, column=1)
        self.entry_page_size.insert(0, "1000")

        row += 1

        self.label_bucket_size = tk.Label(master, text="Bucket Size:")
        self.label_bucket_size.grid(row=row, column=0, sticky="e")

        self.entry_bucket_size = tk.Entry(master)
        self.entry_bucket_size.grid(row=row, column=1)
        self.entry_bucket_size.insert(0, "905")

        row += 1

        # Action Buttons Section
        self.generate_table_button = tk.Button(
            master,
            text="Generate Table Structures",
            command=self.generate_table_structures,
        )
        self.generate_table_button.grid(row=row, column=0, columnspan=3)

        row += 1

        # Results Section
        self.result_area = scrolledtext.ScrolledText(master, height=10)
        self.result_area.grid(row=row, column=0, columnspan=3)

    def generate_table_structures(self):
        self.result_area.delete("1.0", tk.END)
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
            f"Table and Hash Table structures have been generated.\n",
        )
        self.result_area.insert(
            tk.END,
            f"Page Size: {page_size} - Page Count: {self.table_instance.get_pages_count()}\n",
        )
        self.result_area.insert(
            tk.END,
            f"Bucket Size: {bucket_size} - Bucket Count: {self.hash_table_instance.get_bucket_count()}\n",
        )
        self.result_area.insert(tk.END, f"{'-'*20}\n")
        self.result_area.insert(
            tk.END,
            f"Collisions: {self.hash_table_instance.get_collisions()} ({self.hash_table_instance.get_collisions()*100/ len(self.table_instance):.5f}%)\n",
        )
        self.result_area.insert(
            tk.END,
            f"Overflows: {self.hash_table_instance.get_overflows()} ({(self.hash_table_instance.get_overflows() * 100)/ self.hash_table_instance.get_bucket_count():.5f}%)",
        )
        self.search_button["state"] = "normal"

        self.head_button["state"] = "normal"

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

    def head(self):
        self.result_area.delete("1.0", tk.END)
        head_size = int(self.head_size.get())

        if self.table_instance is None or self.hash_table_instance is None:
            self.result_area.insert(
                tk.END, "Please generate table structures before searching.\n"
            )
            return

        line_count = 0
        for page in self.table_instance._pages:
            for tuple in page.get_page():
                if line_count == head_size:
                    return
                self.result_area.insert(
                    tk.END, f"{line_count + 1} - {tuple.get_value()}\n"
                )
                line_count += 1


if __name__ == "__main__":
    root = tk.Tk()
    gui = WordSearchGUI(root)
    root.mainloop()
