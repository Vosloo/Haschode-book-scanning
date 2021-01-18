from tqdm import tqdm
from random import sample, random
from typing import List
from copy import copy
import numpy as np
from math import ceil

from solution import Solution
from storage import Storage
from greedy import get_books


# initialization of population [creating first population]
def initialization(pop_size, storage: Storage, greedy_injection):
    if greedy_injection:
        pop = [
            Solution(sample(range(storage.lib_count), storage.lib_count))
            for _ in range(pop_size - len(greedy_injection))
        ]
        pop.extend(greedy_injection)
        return pop
    else:
        return [
            Solution(sample(range(storage.lib_count), storage.lib_count))
            for _ in range(pop_size)
        ]

# fitness function
def fitness(population: List[Solution], storage: Storage):
    for solution in population:
        score, day, idx = [0, 0, 0]
        scanned_books = set()

        while idx < len(solution):
            lib = storage[solution[idx]]
            day += lib.signup_time

            if day >= storage.no_days:
                break

            avl_books = get_books(
                lib.books,
                scanned_books,
                storage.no_days - day,
                lib.no_books_day,
            )

            score += sum([storage.book_scores[i] for i in avl_books])
            scanned_books.update(avl_books)
            idx += 1

        solution.genotype = solution.genotype[:idx]
        solution.set_score(score)


# roulette selection of parents
def parent_selection(pop_size, population: List[Solution]):
    p = np.array([float(solution.score) for solution in population])
    p /= p.sum()
    pop_range = list(range(pop_size))
    return [
        np.random.choice(a=pop_range, size=2, replace=False, p=p)
        for _ in range(pop_size)
    ]


# order one crossover
def crossover(pairs, population: List[Solution]):
    new_population = list()

    for pair in pairs:
        p1, p2 = copy(population[pair[0]].genotype), copy(population[pair[1]].genotype)
        p1_set, p2_set = set(p1), set(p2)

        p1 += [i for i in p2_set if i not in p1_set]
        p2 += [i for i in p1_set if i not in p2_set]

        length = len(p1)

        start = length // 4

        part = p1[start : start + length // 2]
        part_set = set(part)
        rest_part = [i for i in p2 if i not in part_set]

        # child
        new_population.append(Solution(rest_part[:start] + part + rest_part[start:]))

    return new_population

# swap mutation with mutation probability factor mutation_prob
def mutation(new_population: List[Solution], mutation_prob, no_mutations):
    for solution in new_population:
        if random() < mutation_prob:
            to_swap = [
                sample(range(len(solution)), 2)
                for _ in range(ceil(len(solution) * no_mutations))
            ]
            for swap in to_swap:
                solution[swap[0]], solution[swap[1]] = (
                    solution[swap[1]],
                    solution[swap[0]],
                )


# elite is number of best solutions (based on fitness) that will be transfered to next population
def population_selection(
    pop_size, population: List[Solution], new_population: List[Solution], elite
):
    mixed_populations = population + new_population
    p = np.array([float(solution.score) for solution in mixed_populations])
    p /= p.sum()
    mixed_pop_range = list(range(pop_size * 2))

    # choosing population size - elite of solution that will be moved to next population
    # number of elite places (in next_population) reserved for the best scores to ensure their survival (elite < pop_size)
    next_population_choice = np.random.choice(
        a=mixed_pop_range, size=pop_size - elite, p=p
    )
    next_population = [mixed_populations[i] for i in next_population_choice]

    # picking elite
    mixed_populations.sort(key=lambda x: x.score, reverse=True)
    next_population.extend(mixed_populations[:elite])

    return next_population

# genetic function returns best solution in population in the last generation
def genetic(
    storage: Storage,
    no_generations,
    pop_size,
    elite,
    mutation_prob,
    no_mutations,
    greedy_injection=None,
):
    population = initialization(pop_size, storage, greedy_injection)
    fitness(population, storage)

    for _ in tqdm(range(no_generations)):
        pairs = parent_selection(pop_size, population)
        new_population = crossover(pairs, population)
        mutation(new_population, mutation_prob, no_mutations)
        fitness(new_population, storage)
        population = population_selection(pop_size, population, new_population, elite)

    return max(population, key=lambda x: x.score)