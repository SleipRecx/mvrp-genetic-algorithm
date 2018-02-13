import random
import time
from src.chromosome import Chromosome
from src.util import read_problem_file
from pprint import pprint


class Population:
    def __init__(self, customers, depots, max_vehicles, size: int = 200):
        self.customers = customers
        self.depots = depots
        self.max_vehicles = max_vehicles
        self.population = [Chromosome(self.customers, self.depots, self.max_vehicles) for _ in range(size)]

    def evolve(self):
        new_population = []
        elites = self.get_fittest(self.population, 2)
        new_population.extend(elites)
        while len(new_population) <= len(self.population) - 2:
            tournament = random.sample(self.population, random.randint(2, 5))
            winners = self.get_fittest(tournament, 2)
            p1 = winners[0]
            p2 = winners[1]
            c1, c2 = Chromosome.crossover(p1, p2)
            c1.mutation()
            c2.mutation()
            new_population.extend([c1, c2])
        self.population = new_population
        best = self.get_fittest(self.population, 1)[0]
        print("Distance:", best.calculate_distance())
        print("Load:", best.calculate_excess_load())

    @staticmethod
    def get_fittest(individuals: list, number: int) -> list:
        assert number <= len(individuals)
        fitness_sorted = sorted(individuals, key=lambda x: x.calculate_fitness(), reverse=True)
        return fitness_sorted[0:number]


if __name__ == '__main__':
    c, d, m = read_problem_file("../data/problem/p23")
    population = Population(c, d, m)
    start = time.time()
    for i in range(1, 500):
        population.evolve()

    print(time.time() - start)
