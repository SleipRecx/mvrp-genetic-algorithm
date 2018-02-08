import random
import time
from src.chromosome import Chromosome
from src.util import read_problem_file, plot


class Population:
    def __init__(self, customers, depots, max_vehicles, size: int = 100):
        self.customers = customers
        self.depots = depots
        self.max_vehicles = max_vehicles
        self.population = [Chromosome(self.customers, self.depots, self.max_vehicles) for _ in range(size)]

    def evolve(self):
        new_population = []
        for _ in range(len(self.population) // 2):
            tournament = random.sample(self.population, random.randint(5, len(self.population)))
            winners = self.get_fittest(tournament, 2)
            p1 = winners[0]
            p2 = winners[1]
            c1, c2 = Chromosome.crossover(p1, p2)
            c1.intra_depot_mutation()
            c2.intra_depot_mutation()
            new_population.extend([c1, c2])
        self.population = new_population
        best = self.get_fittest(self.population, 1)[0]
        print(best.calculate_distance())

    # top_1 = self.get_fittest(self.individuals, int(0.01 * len(self.individuals)))
    # replace_indices = random.sample(list(range(len(new_population))), len(top_1))
    # for i, index in enumerate(replace_indices):
    #     new_population[index] = top_1[i]

    @staticmethod
    def get_fittest(individuals: list, number: int) -> list:
        assert number <= len(individuals)
        fitness_sorted = sorted(individuals, key=lambda x: x.calculate_fitness(), reverse=True)
        return fitness_sorted[0:number]


if __name__ == '__main__':
    c, d, m = read_problem_file("../data/problem/p01")
    population = Population(c, d, m)
    start = time.time()
    for i in range(100):
        population.evolve()
    print(time.time() - start)

