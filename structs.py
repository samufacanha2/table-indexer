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


class table:
    _pages: List[List[tuple]] = []

    def __init__(self, words: List[str]) -> None:
        tuples = []
        for i, word in enumerate(words):
            tuples.append(tuple(i, word))
        self._pages = [
            tuples[i : i + PAGE_SIZE] for i in range(0, len(tuples), PAGE_SIZE)
        ]

    def get_page_items(self, page: int) -> List[tuple]:
        return self._pages[page]


BUCKET_SIZE = 100


def hash_function(value, table) -> int:
    return sum([(ord(c) - ord("a")) * (i + 1) for i, c in enumerate(value)]) % (
        BUCKET_SIZE * len(table._pages) * PAGE_SIZE
    )


class bucket:
    _hashes_and_refs = []  # [[hash1, [ref1,ref2]], [hash2, [ref3]], ...]

    def __init__(self) -> None:
        self._hashes_and_refs = []

    def add_ref_to_hash(
        self, hash: int, ref: int
    ) -> bool:  # return true if there is a collision
        for hash_and_ref in self._hashes_and_refs:
            if hash_and_ref[0] == hash:
                hash_and_ref[1].append(ref)
                return True
        if len(self._hashes_and_refs) < BUCKET_SIZE:
            self._hashes_and_refs.append([hash, [ref]])
        return False

    def is_full(self) -> bool:
        return len(self._hashes_and_refs) == BUCKET_SIZE

    def get_refs(self, hash: int) -> List[int]:
        for hash_and_ref in self._hashes_and_refs:
            if hash_and_ref[0] == hash:
                return hash_and_ref[1]
        return []


class indexed_table:
    _buckets = []
    _collisions = 0
    _table = table([])

    def __init__(self, table: table) -> None:
        buckets = [
            bucket() for _ in range(len(table._pages) * PAGE_SIZE // BUCKET_SIZE + 1)
        ]
        print(len(buckets))
        for page in table._pages:
            for tuple in page:
                hash = hash_function(tuple.get_value(), table)
                collides = buckets[hash].add_ref_to_hash(hash, tuple.get_index())
                if collides:
                    self._collisions += 1
        self._buckets = buckets
        self._table = table
        # print(self._collisions)
        # print(buckets[99]._hashes_and_refs)

    def find_word(self, word: str):
        start_time = time.time()
        hash = hash_function(word, self._table)
        refs = self._buckets[hash].get_refs(hash)
        for ref in refs:
            if (
                self._table.get_page_items(ref // PAGE_SIZE)[
                    ref % PAGE_SIZE
                ].get_value()
                == word
            ):
                return [ref, time.time() - start_time]
        return [None, time.time() - start_time]
