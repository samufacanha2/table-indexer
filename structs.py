import time
from typing import List

PAGE_SIZE = 1000


class tuple:
    _index = -1
    _value = ""

    def __init__(self, index, value):
        self._index = index
        self._value = value

    def get_value(self) -> str:
        return self._value

    def get_index(self) -> int:
        return self._index


class page:
    _tuples: List[tuple] = []

    def __init__(self, tuples: List[tuple]) -> None:
        self._tuples = tuples

    def get_tuple(self, index: int) -> tuple:
        return self._tuples[index]

    def get_page(self) -> List[tuple]:
        return self._tuples


class table:
    _pages: List[page] = []

    def __init__(self, words: List[str]) -> None:
        tuples = []

        for i, word in enumerate(words):
            tuples.append(tuple(i, word))
            if len(tuples) == PAGE_SIZE:
                self._pages.append(page(tuples))
                tuples = []

        if len(tuples) > 0:
            self._pages.append(page(tuples))

    def get_page(self, page: int) -> List[tuple]:
        return self._pages[page].get_page()

    def get_pages_count(self) -> int:
        return len(self._pages)

    def __len__(self) -> int:
        return len(self._pages) * PAGE_SIZE


BUCKET_SIZE = 100


def hash_function(value, table) -> int:
    return sum([(ord(c) - ord("a")) * (i + 1) for i, c in enumerate(value)]) % (
        len(table) // BUCKET_SIZE + 1
    )


class bucket:
    _words: List[str] = []
    _pages: List[int] = []

    _next = None

    def __init__(self) -> None:
        self._words = []
        self._pages = []
        self._next = None

    def add(self, word: str, page: int) -> List[bool]:
        had_collision, had_overflow = False, False
        if len(self._words) == BUCKET_SIZE:
            if self._next == None:
                self._next = bucket()
                had_overflow = True
            self._next.add(word, page)
            had_collision = True
            return [had_collision, had_overflow]
        self._words.append(word)
        self._pages.append(page)
        return [had_collision, had_overflow]

    def get_page(self, word: str) -> int:
        if word in self._words:
            return self._pages[self._words.index(word)]
        if self._next != None:
            return self._next.get_page(word)
        return -1


class hash_table:
    _buckets: List[bucket] = []
    _table = None
    _collisions = 0
    _overflows = 0

    def __init__(self, table: table) -> None:
        self._buckets = [bucket() for _ in range(len(table) // BUCKET_SIZE + 1)]
        self._table = table

        for page_index, page in enumerate(table._pages):
            for tuple in page.get_page():
                index = hash_function(tuple.get_value(), table)
                [had_collision, had_overflow] = self._buckets[index].add(
                    tuple.get_value(), page_index
                )
                if had_collision:
                    self._collisions += 1
                if had_overflow:
                    self._overflows += 1
        print(f"{self._collisions} collisions, {self._overflows} overflows")

    def get_word_page(self, word: str):
        if self._table is None:
            return -1
        index = hash_function(word, self._table)
        return self._buckets[index].get_page(word)

    def get_word_tuple(self, word: str):
        memory_access_count = 0
        start_time = time.time()
        page = self.get_word_page(word)
        if page == -1:
            return [None, time.time() - start_time, memory_access_count]

        if self._table is None:
            return [None, time.time() - start_time, memory_access_count]

        memory_access_count += 1
        for tuple in self._table.get_page(page):
            if tuple.get_value() == word:
                return [tuple, time.time() - start_time, memory_access_count]

        return [None, time.time() - start_time, memory_access_count]
