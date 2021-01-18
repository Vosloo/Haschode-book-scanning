import os
from copy import copy
from math import ceil
from time import perf_counter

from storage import Storage
from solution import Solution

from greedy import greedy, get_books
from genetic import genetic, fitness

# mutation_prob - probability of mutation of given child (solution)
# no_mutations - number of mutation swaps (percentage of length of solution genotype)
# injection - boolean (when set to True greedy solutions added to initial population) default: True
# since there is a time constraint it is recomended to leave it at default (injection yields better results)
input_path = "./data"
output_path = "./solutions"
mutation_prob = 0.05
no_mutations = 0.06
injection = True


# elite_multiplier - elite coefficient of pop_size (elite - number of best solutions passed to next population)
# injection_multiplier - injection coefficient of pop_size (injection - number of greedy solutions passed to initial population)
elite_multiplier = 0.01
injection_multiplier = 0.1

# since there is a time constraint it would be unwise to set population size and number of generations same for file
# files are split into 3 categories: small, medium and large with idea of connecting "heavy" files to lower categories
# (heavy in context of complexity of input data)
genetic_params = {
    "small": {"pop_size": 200, "no_generations": 5},
    "medium": {"pop_size": 300, "no_generations": 5},
    "large": {"pop_size": 1200, "no_generations": 5},
}

# blacklisted - list of files to skip (in order to blacklist a file insert 1 letter, it works only if all files are starting with different letter)
# skip_genetic - list of files that skip genetic algorithms (works as blacklist - takes 1 letter). In primary testing conclusion was made:
# in given time limit, when injecting greedy solution, final solution of genetic algorithm is "always" greedy solution (after 50 runs yet to observe diffrent result)
# in order to gain some time genetic algorithm skips file a_example.txt, b_read_on.txt and c_incunabula (for file a its because greedy is already best solutuion)
blacklisted = []
skip_genetic = ["a", "b", "c"]

# function to save results
def save_result(solution: Solution, storage: Storage, FILE):
    to_write = list()
    scanned_books = set()
    day = 0

    to_write.append(f"{len(solution)}\n")

    for lib_idx in solution.genotype:
        lib = storage[lib_idx]
        day += lib.signup_time

        avl_books = get_books(
            lib.books, scanned_books, storage.no_days - day, lib.no_books_day
        )

        to_write.append(f"{lib_idx} {len(avl_books)}\n")
        to_write.append(" ".join(list(map(str, avl_books))) + "\n")

        scanned_books.update(avl_books)

    with open(f"{output_path}/{FILE}", "w+") as f:
        f.writelines(to_write)


if __name__ == "__main__":
    s = perf_counter()

    total_score = 0

    for FILE in os.listdir(input_path):

        startswith = FILE[0]

        if not FILE.endswith(".txt") or startswith in blacklisted:
            continue

        # saving file data to Storage
        storage = Storage(f"{input_path}/{FILE}")

        if startswith in ["a", "d"]:
            params = genetic_params["small"]
        elif startswith in ["b", "c", "e"]:
            params = genetic_params["medium"]
        elif startswith == "f":
            params = genetic_params["large"]
        else:
            params = genetic_params["small"]

        # elite - number of best solutions passed to next population
        elite = ceil(params["pop_size"] * elite_multiplier)

        if injection:
            # greedy algorithm takes too much time on d_tough_choices.txt. Used simplified version
            if FILE.startswith("d"):
                greedy_solution = Solution(
                    sorted(
                        list(range(storage.lib_count)),
                        key=lambda x: len(storage[x]),
                    )
                )
            else:
                greedy_solution = greedy(storage)

            if startswith in skip_genetic:
                solution = greedy_solution
            else:
                # injecting greedy solution to initial population of genetic algorithm
                _injections = ceil(params["pop_size"] * injection_multiplier)
                greedy_injection = [copy(greedy_solution) for _ in range(_injections)]

                solution = genetic(
                    storage,
                    params["no_generations"],
                    params["pop_size"],
                    elite,
                    mutation_prob,
                    no_mutations,
                    greedy_injection,
                )

            fitness([greedy_solution], storage)
            # print(f"{FILE} [greedy] score: {greedy_solution.score}")
        else:
            solution = genetic(
                storage,
                params["no_generations"],
                params["pop_size"],
                elite,
                mutation_prob,
                no_mutations,
            )

        print(f"{FILE} Score: {solution.score}\n")

        save_result(solution, storage, FILE)

        total_score += solution.score

    print(f"Time: {perf_counter() - s}")
    print(f"Total score: {total_score}")