import time

from population import Population
from util import read_problem_file


PROBLEM = "p01"
POPULATION_SIZE = 100
GENERATIONS = 250
CROSSOVER_PROBABILITY = 0.8
INTRA_DEPOT_PROBABILITY = 0.2
INTER_DEPOT_PROBABILITY = 0.2


def main():
    c, d, m = read_problem_file("../data/problem/" + PROBLEM)
    population = Population(customers=c,
                            depots=d,
                            max_vehicles=m,
                            size=POPULATION_SIZE,
                            p_crossover=CROSSOVER_PROBABILITY,
                            p_intra=INTRA_DEPOT_PROBABILITY,
                            p_inter=INTER_DEPOT_PROBABILITY)
    for _ in range(0, GENERATIONS):
        population.evolve()


if __name__ == '__main__':
    main()
