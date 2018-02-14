import time

from population import Population
from util import read_problem_file, timeit, write_results_to_file

PROBLEM = "p01"
POPULATION_SIZE = 100
GENERATIONS = 250
ELITES = 4
CROSSOVER_PROBABILITY = 0.8
INTRA_DEPOT_PROBABILITY = 0.2
INTER_DEPOT_PROBABILITY = 0.02


@timeit
def main():
    c, d, m = read_problem_file("../data/problem/" + PROBLEM)
    population = Population(customers=c,
                            depots=d,
                            max_vehicles=m,
                            size=POPULATION_SIZE,
                            p_crossover=CROSSOVER_PROBABILITY,
                            p_intra=INTRA_DEPOT_PROBABILITY,
                            p_inter=INTER_DEPOT_PROBABILITY,
                            elites=ELITES)
    try:
        for generation in range(0, GENERATIONS):
            population.evolve()
            print("generation:", generation)
            population.print_summary()
    except KeyboardInterrupt:
        print("\nAborting")
    finally:
        print(population.print_summary())
        write_results_to_file(population.best, PROBLEM + "-" + str(int(population.best.calculate_distance())))


if __name__ == '__main__':
    main()
