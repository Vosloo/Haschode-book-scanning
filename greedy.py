import os
from time import time
from tqdm import tqdm
from random import sample
from typing import List

from library import Library
from solution import Solution
from storage import Storage


data_dir = "data/"


# returns best books based on their scores, days left and library books bandwidth
def get_books(lib_books, scanned_books, days_left, lib_bandwidth):
    return [i for i in lib_books if i not in scanned_books][: days_left * lib_bandwidth]


# returns library with the best score
def get_library(libraires_left, storage: Storage, days_left, scanned_books):
    max_library = None
    max_library_score = float("-inf")
    books_scores = storage.weights

    # for idx in libraires_left:
    #     lib = storage[idx]

    #     avl_books = get_books(
    #         lib.books,
    #         scanned_books,
    #         days_left - lib.days_to_sign,
    #         lib.daily_scans,
    #     )

    #     lib_score = len(avl_books)

    #     # lib_score = sum(books_scores[i] for i in avl_books) / lib.days_to_sign

    #     if lib_score > max_library_score:
    #         max_library_score = lib_score
    #         max_library = idx

    return 0


def greedy(storage: Storage):
    scanned_books = set()
    libraires_left = set(range(storage.lib_count))
    day = 0
    solution = list()

    for _ in tqdm(range(storage.lib_count)):

        next_library = get_library(
            libraires_left, storage, storage.days_avail - day, scanned_books
        )

        lib = storage[next_library]

        day += lib.days_to_sign

        if day >= storage.days_avail:
            break

        libraires_left.discard(next_library)
        solution.append(next_library)

        scanned_books.update(
            get_books(
                lib.books, scanned_books, storage.days_avail - day, lib.daily_scans,
            )
        )

    return Solution(solution)


def fitness(population: List[Solution], storage: Storage):
    for solution in population:
        score, cur_time, idx = [0, 0, 0]
        scanned_books = set()

        genotype = solution.queue

        while idx < len(genotype) and cur_time < storage.days_avail:
            cur_lib = storage.libraries[genotype[idx]]
            cur_time += cur_lib.days_to_sign

            if cur_time < storage.days_avail:
                # list of books to be shiped from given library
                books_avail = [i for i in cur_lib.books if i not in scanned_books][
                    : (storage.days_avail - cur_time) * cur_lib.daily_scans
                ]

                score += sum([storage.weights[i] for i in books_avail])

                scanned_books.update(books_avail)

            idx += 1

        solution.queue = solution.queue[:idx]
        solution.set_score(score)


if __name__ == "__main__":
    total_score = 0
    for FILE in os.listdir("./data"):
        if not FILE.endswith(".txt"):
            continue

        storage = Storage(data_dir + FILE)

        print(data_dir + FILE)

        # solution = greedy(storage)
        if FILE.startswith("d"):
            solution = Solution(
                sorted(
                    list(range(storage.lib_count)),
                    key=lambda lib_ind: len(storage[lib_ind]),
                )
            )

        fitness([solution], storage)

        print(f"{solution.score}")
