import os
from random import sample

from storage import Storage
from solution import Solution


data_dir = 'data/'
pop_size = 100
generations = 100


def _cross(pair):
    pass


def crossover(parents):
    for pair in parents:
        child = _cross(pair)
        yield child


def mutation(child):
    pass


def _get_score(lib):
    pass


def fitness(population: list[Solution]):
    for ind, pop in enumerate(population):
        libraries = pop.queue
        score = 0
        scanned_books = set()
        cur_day = 0
        for lib in libraries:
            if scan_day := cur_day + storage[lib].sign_proc >= storage.days:
                break
            # days = 3
            # cur_day = 0
            # sign_proc = 2
            # days - (cur_day + sign_proc) * daily_scans


        population[ind].set_score(score)


def selection(population):
    no_pairs = len(population)
    pairs = []
    for i in range(no_pairs):
        pairs.append(sample(population, 2))

    return pairs


def select_best(old_pop, new_pop):
    pass


if __name__ == "__main__":
    for file in os.listdir(data_dir):
        storage = Storage(data_dir + file)
        
        population = [
            Solution(sample(range(0, storage.lib_count), storage.lib_count))
            for _ in range(pop_size)
        ]

        for no_gen in range(generations):
            new_population = []
            fitness(population)
            parents = selection(population)
            for i in range(len(population)):
                child = crossover(parents)
                mutation(child)

                new_population.append(child)
            
            population = select_best(population, new_population)
        