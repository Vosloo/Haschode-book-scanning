from library import Library
import os
from random import sample, uniform, randint
from typing import List
from tqdm import tqdm

from storage import Storage
from solution import Solution


data_dir = 'data/'
pop_size = 2000
generations = 20
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


def fitness(population: List[Solution], storage: Storage):
    for solution in population:
        score, cur_time, idx = [0, 0, 0]
        scanned_books = set()

        genotype = solution.queue

        while (idx < len(genotype) and cur_time < storage.days_avail):
            cur_lib = storage.libraries[genotype[idx]]
            cur_time += cur_lib.days_to_sign
            
            if (cur_time < storage.days_avail):
                # list of books to be shiped from given library
                books_avail = [i for i in cur_lib.books if i not in scanned_books][:(storage.days_avail - cur_time) * cur_lib.daily_scans]

                score += sum([storage.weights[i] for i in books_avail])

                scanned_books.update(books_avail)
            
            idx += 1

        solution.set_score(score)


def selection(population: List[Solution]) -> List[Solution]:
    no_pairs = len(population)
    pairs = []
    for i in range(no_pairs):
        pairs.append(sample(population, 2))

    return pairs


def select_best(old_pop: List[Solution], new_pop: List[Solution]):
    # Create new population from original and new ones sorting by score
    final_pop = sorted(
        old_pop + new_pop, key=lambda item: item.score, reverse=True
    )

    # Return only 'n' sized pop as the original one
    return final_pop[:len(old_pop)]


def save_solution(solution: Solution, storage: Storage):
    no_libs = len(solution)

    cur_time, idx = [0, 0]
    scanned_books = set()

    genotype = solution.queue

    libs = []
    while (idx < no_libs and cur_time < storage.days_avail):
        cur_lib = storage.libraries[genotype[idx]]
        cur_time += cur_lib.days_to_sign
        
        if (cur_time < storage.days_avail):
            # list of books to be shiped from given library
            books_avail = [i for i in cur_lib.books if i not in scanned_books][:(storage.days_avail - cur_time) * cur_lib.daily_scans]

            scanned_books.update(books_avail)
        
            libs.append(f"{genotype[idx]} {len(books_avail)}\n")
            libs.append(" ".join(list(map(str, books_avail))) + '\n')

        idx += 1

    sol_file = storage.file_name.split('/')[1]
    with open("solutions/" + sol_file, 'w+') as sfile:
        # no_libs
        sfile.write(f"{int(len(libs) / 2)}\n")
        sfile.writelines(libs)


if __name__ == "__main__":
    total_score = 0
    for FILE in os.listdir('./data'):
        # Skip non-input files and d (since that's too slow)
        if not FILE.endswith('.txt'):# or FILE.startswith('d'):
            continue

        storage = Storage(data_dir + FILE)

        print(data_dir + FILE)
    
        # Create random population
        population = [
            Solution(sample(range(storage.lib_count), storage.lib_count))
            for _ in range(pop_size)
        ]

        # Set score for every library
        fitness(population, storage)

        # for no_gen in tqdm(range(generations)):
        #     # print(f"No. gen: {no_gen}")
        #     new_population = []

        #     # Create no pairs of parents for crossover
        #     parents = selection(population)

        #     for child in crossover(parents):
        #         # Create 'n' children and mutate (some of) them
        #         # mutation(child)

        #         new_population.append(child)

        #     fitness(new_population, storage)
            
        #     # Select new population from set of old and new one
        #     population = select_best(population, new_population)
            
        best_solution = max(population, key=lambda sol: sol.score)

        save_solution(best_solution, storage)

        total_score += best_solution.score

        print(f"Total score: {best_solution.score}")
    
    print(f"Total final score: {total_score}")