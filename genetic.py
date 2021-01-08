from library import Library
import os
from random import sample, uniform, randint
from typing import List

from storage import Storage
from solution import Solution


data_dir = 'data/'
pop_size = 100
generations = 10
mutation_chance = 5 # in %


# [12, 1, 2, 6, 9] -> size: 5 -> 2 (1st) / 3 (2nd) -> [12, 1]
# [8, 1, 7, 12, 11] -> [8, 7, 11] 
# 


def _cross(pair: List[Solution]) -> Solution:
    p1, p2 = pair
    size_1 = len(p1) // 2
    size_2 = len(p1) - size_1
    
    first = set(sample(p1.queue, size_1))
    second = sample(set(p2.queue) - first, size_2)

    return Solution([*first, *second])


def crossover(parents) -> Solution:
    for pair in parents:
        child = _cross(pair)
        yield child


def mutation(child: Solution):
    mutate = uniform(1, 100) <= mutation_chance
    if mutate:
        # Change <1; 15% * len(child)> positions of libraries
        count = randint(1, 15 * len(child) // 100)

        to_change = sample(child, count*2)
        for i in range(size := len(to_change)):
            # size is always even
            ind_1, ind_2 = i, (size / 2) + i
            first, second = to_change[ind_1], to_change[ind_2]
            child[first], child[second] = child[second], child[first]


def _get_books(storage: Storage):
    """
    Scans best books from already signed libraries, picking the best ones and
    from the libraries according to the order they were signed, increments
    current day and returns score of scanned books.
    """
    score = 0
    for signed_lib in storage.signed_libs:
        no_books = storage[signed_lib].daily_scans

        available_books = set(range(len(storage.weights)))
        available_books -= set(storage.scanned)

        # All books scanned
        if not available_books:
            break

        # available_weights = [storage.weights[book] for book in available_books]
        available_weights = {book: storage.weights[book] for book in available_books}
        for i in range(no_books):
            # Get book (not weight) with maximum score
            book = max(available_weights, key=lambda k: available_weights[k])
            
            weight = available_weights[book]
            score += weight
            
            # Add it to already scanned
            storage.add_scanned_book(book)

            # Delete it from library, not to scan it again
            del available_weights[book]

    # Increase current day
    storage.cur_day += 1

    # Decrease left signing time for currently signing library
    if storage.currently_signing != -1:
        lib = storage.currently_signing
        storage[lib].days_to_sign -= 1

        # If signing process has ended...
        if storage[lib].days_to_sign == 0:
            storage.currently_signing = -1
            storage.signed_libs.append(lib)

    return score


def _get_score(libraries: List, storage: Storage):
    """
    Returns score of libraries based on:
    current day, days avaialbe, daily scans, position in queue.
    """
    score = 0
    while libraries:
        lib_ind = libraries[0]
        # library = storage[lib_ind]

        if storage.currently_signing == -1:
            storage.currently_signing = lib_ind
            
            # Delete currently signing library from queue
            libraries.pop(0)

        # Get books from already signed libraries
        score += _get_books(storage)

    # Already signed all libraries (that had enough time for signing)\
    while storage.cur_day < storage.days_avail and \
            len(storage.scanned) < storage.book_count:
        score += _get_books(storage)

    return score


def _get_no_libs(storage: Storage, libraries):
    """
    Get number of libraries that can be processed during the time we have (days)
    """
    cur_days = 0
    no_libs = 0
    for lib in libraries:
        if cur_days + storage[lib].sign_proc >= storage.days_avail:
            return no_libs
        
        cur_days += storage[lib].sign_proc
        no_libs += 1

    return no_libs


def fitness(population: List[Solution], storage: Storage):
    for ind, pop in enumerate(population):
        libraries = pop.queue
        
        no_libs = _get_no_libs(storage, libraries)
        libraries = libraries[:no_libs]
        
        score = _get_score(libraries, storage)

        population[ind].set_score(score)


def selection(population: List[Solution]) -> List[Solution]:
    no_pairs = len(population)
    pairs = []
    for i in range(no_pairs):
        pairs.append(sample(population, 2))

    return pairs


def select_best(old_pop: List[Solution], new_pop: List[Solution]):
    # Create new population from original and new ones sorting by score
    final_pop = sorted(
        [*old_pop, *new_pop], key=lambda item: item.score, reverse=True
    )

    # Return only 'n' sized pop as the original one
    return final_pop[:len(old_pop)]


if __name__ == "__main__":
    # for file in os.listdir(data_dir):
    storage = Storage(data_dir + "a_example.txt")
    
    # Create random population
    population = [
        Solution(sample(range(0, storage.lib_count), storage.lib_count))
        for _ in range(pop_size)
    ]

    for no_gen in range(generations):
        print(no_gen)
        new_population = []

        # Set score for every library
        fitness(population, storage)

        # Create no pairs of parents for crossover
        parents = selection(population)

        for child in crossover(parents):
            # Create 'n' children and mutate (some of) them
            mutation(child)

            new_population.append(child)
        
        # Select new population from set of old and new one
        population = select_best(population, new_population)
        