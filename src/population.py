from src.chromosome import Chromosome
from src.util import read_problem_file


class Population:
    def __init__(self, customers, depots, max_vehicles, size: int = 100):
        self.individuals = [Chromosome(customers, depots, max_vehicles) for _ in range(size)]
        Chromosome.crossover(self.individuals[0], self.individuals[1])

    def get_fittest(self, number: int) -> list:
        assert number <= len(self.individuals)
        fitness_sorted = sorted(self.individuals, key=lambda x: x.calculate_fitness(), reverse=True)
        return fitness_sorted[0:number]


if __name__ == '__main__':
    c, d, m = read_problem_file("../data/problem/p01")
    population = Population(c, d, m, 100)
    population.get_fittest(1)[0].intra_depot_swapping()
