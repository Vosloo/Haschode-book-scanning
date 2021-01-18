from tqdm import tqdm

from solution import Solution
from storage import Storage

# returns best books based on their scores, days left and library books bandwidth -- number_of_days_left * library_throughput (number of books that it can ship a day)
# books are already sorted and only theese that are not yet scaanned are taken into consideration
def get_books(lib_books, scanned_books, days_left, lib_no_books_day):
    return [i for i in lib_books if i not in scanned_books][
        : days_left * lib_no_books_day
    ]


# returns library with the best score
def get_library(libraires_left, storage: Storage, days_left, scanned_books):
    max_lib_idx = None
    max_lib_score = float("-inf")

    for lib_idx in libraires_left:
        lib = storage[lib_idx]
        book_scores = storage.book_scores
        avl_books = get_books(
            lib.books,
            scanned_books,
            days_left - lib.signup_time,
            lib.no_books_day,
        )

        lib_score = sum(book_scores[i] for i in avl_books) / lib.signup_time

        if lib_score > max_lib_score:
            max_lib_score = lib_score
            max_lib_idx = lib_idx

    return max_lib_idx


def greedy(storage: Storage):
    scanned_books = set()
    libraires_left = set(range(storage.lib_count))
    solution = list()
    day = 0

    for _ in tqdm(range(storage.lib_count)):
        next_lib = get_library(
            libraires_left, storage, storage.no_days - day, scanned_books
        )

        lib = storage[next_lib]

        day += lib.signup_time

        if day >= storage.no_days:
            break

        libraires_left.discard(next_lib)
        solution.append(next_lib)

        scanned_books.update(
            get_books(
                lib.books,
                scanned_books,
                storage.no_days - day,
                lib.no_books_day,
            )
        )

    return Solution(solution)