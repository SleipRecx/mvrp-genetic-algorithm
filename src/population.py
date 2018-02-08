import random
from src.chromosome import Chromosome
from src.util import read_problem_file, plot


class Population:
    def __init__(self, customers, depots, max_vehicles):
        self.customers = customers
        self.depots = depots
        self.max_vehicles = max_vehicles
        self.individuals = []

    def genetic_algorithm(self, size: int = 100, generations: int = 100):
        self.individuals = [Chromosome(self.customers, self.depots, self.max_vehicles) for _ in range(size)]
        # fitness_list = list(map(lambda x: x.calculate_fitness(), self.individuals))
        # average_fitness = sum(fitness_list) / len(fitness_list)
        for generation in range(generations):
            new_population = []
            fittest = self.get_fittest(self.individuals, 1)[0]
            # print(fittest.calculate_distance())
            # if fittest.calculate_distance() < 1000:
            #     plot(fittest)
            #     return
            while len(new_population) < size:
                tournament = random.sample(self.individuals, random.randint(5, len(self.individuals)))
                winners = self.get_fittest(tournament, 2)
                p1 = winners[0]
                p2 = winners[1]
                c1, c2 = Chromosome.crossover(p1, p2)
                c1.intra_depot_mutation()
                c2.intra_depot_mutation()
                new_population.extend([c1, c2])
            self.individuals = new_population
        fitness_list = list(map(lambda x: x.calculate_fitness(), self.individuals))
        average_fitness = sum(fitness_list) / len(fitness_list)
        print(average_fitness)




    @staticmethod
    def get_fittest(individuals: list, number: int) -> list:
        assert number <= len(individuals)
        fitness_sorted = sorted(individuals, key=lambda x: x.calculate_fitness(), reverse=True)
        return fitness_sorted[0:number]


if __name__ == '__main__':
    c, d, m = read_problem_file("../data/problem/p01")
    population = Population(c, d, m)
    population.genetic_algorithm(100)
