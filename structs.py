import time
import math
from typing import List


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
    _page_size = 0

    def __init__(self, words: List[str], page_size: int) -> None:
        self._page_size = page_size
        self._pages = []

        tuples = []

        for i, word in enumerate(words):
            tuples.append(tuple(i, word))
            if len(tuples) == page_size:
                self._pages.append(page(tuples))
                tuples = []

        if len(tuples) > 0:
            self._pages.append(page(tuples))

    def get_page(self, page: int) -> List[tuple]:
        return self._pages[page].get_page()

    def get_pages_count(self) -> int:
        return len(self._pages)

    def __len__(self) -> int:
        return len(self._pages) * self._page_size


def hash_function(value, table, bucket_size) -> int:
    return math.floor(
        sum(
            [
                (ord(c) - ord("0")) * ((i + 1) * math.e) ** 31
                for i, c in enumerate(value)
            ]
        )
        % ((len(table) // bucket_size) + 1)
    )


class bucket:
    _words: List[str] = []
    _pages: List[int] = []
    _bucket_size = 0

    _next = None

    def __init__(self, bucket_size) -> None:
        self._words = []
        self._pages = []
        self._next = None
        self._bucket_size = bucket_size

    def add(self, word: str, page: int) -> List[bool]:
        had_collision, had_overflow = False, False
        if len(self._words) == self._bucket_size:
            if self._next == None:
                had_overflow = True
                self._next = bucket(self._bucket_size)
                self._next.add(word, page)
                return [had_collision, had_overflow]
            _, had_overflow = self._next.add(word, page)
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
    _bucket_size = 0
    _table = None
    _collisions = 0
    _overflows = 0

    def __init__(self, table: table, bucket_size) -> None:
        self._buckets = []
        buckets = [bucket(bucket_size) for _ in range((len(table) // bucket_size) + 1)]
        self._buckets = buckets
        self._table = table
        self._bucket_size = bucket_size
        self._collisions = 0
        self._overflows = 0

        for page_index, page in enumerate(table._pages):
            for tuple in page.get_page():
                index = hash_function(tuple.get_value(), table, bucket_size)
                [had_collision, had_overflow] = buckets[index].add(
                    tuple.get_value(), page_index
                )
                if had_collision:
                    self._collisions += 1
                if had_overflow:
                    self._overflows += 1

    def get_word_page(self, word: str):
        if self._table is None:
            return -1
        index = hash_function(word, self._table, self._bucket_size)
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

    def get_collisions(self) -> int:
        return self._collisions

    def get_overflows(self) -> int:
        return self._overflows

    def get_bucket_count(self) -> int:
        return len(self._buckets)
