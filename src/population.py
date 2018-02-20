import random
from chromosome import Chromosome


class Population:
    def __init__(self, customers, depots, max_vehicles, size, p_crossover, p_inter, p_intra, elites):
        self.customers = customers
        self.depots = depots
        self.max_vehicles = max_vehicles
        self.crossover_probability = p_crossover
        self.intra_depot_probability = p_intra
        self.inter_depot_probability = p_inter
        self.elites = elites
        self.population = [Chromosome(self.customers, self.depots, self.max_vehicles) for _ in range(size)]
        self.best = self.get_fittest(self.population, 1)[0]

    def evolve(self):
        new_population = []
        elites = self.get_fittest(self.population, self.elites)
        new_population.extend(elites)
        for _ in range((len(self.population) - self.elites) // 2):
            tournament = random.sample(self.population, random.randint(2, 2))
            winners = self.get_fittest(tournament, 2)
            p1 = winners[0]
            p2 = winners[1]
            c1, c2 = Chromosome.crossover(p1, p2, self.crossover_probability)
            c1.intra_depot_mutation(self.intra_depot_probability)
            c2.intra_depot_mutation(self.intra_depot_probability)
            c1.inter_depot_mutation(self.inter_depot_probability)
            c2.inter_depot_mutation(self.inter_depot_probability)
            new_population.extend([c1, c2])
        self.population = new_population

    def print_summary(self):
        self.best = self.get_fittest(self.population, 1)[0]
        print("fitness:", self.best.calculate_fitness())
        print("distance:", self.best.calculate_distance()[0])
        print("duration over:", self.best.calculate_distance()[1])
        print("load over", self.best.calculate_excess_load())
        print("-" * 35)

    @staticmethod
    def get_fittest(individuals: list, number: int) -> list:
        assert number <= len(individuals)
        fitness_sorted = sorted(individuals, key=lambda x: x.calculate_fitness(), reverse=True)
        return fitness_sorted[0:number]
