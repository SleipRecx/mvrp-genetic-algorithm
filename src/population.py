from src.chromosome import Chromosome
from src.util import read_problem_file


class Population:
    def __init__(self, customers, depots, max_vehicles, size: int = 100):
        self.individuals = [Chromosome(customers, depots, max_vehicles) for _ in range(size)]


if __name__ == '__main__':
    c, d, m = read_problem_file("../data/problem/p01")
    population = Population(c, d, m, 100)
