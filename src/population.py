import random
from chromosome import Chromosome


class Population:
    def __init__(self, customers, depots, max_vehicles, size, p_crossover, p_inter, p_intra):
        self.customers = customers
        self.depots = depots
        self.max_vehicles = max_vehicles
        self.crossover_probability = p_crossover
        self.intra_depot_probability = p_intra
        self.inter_depot_probability = p_inter
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
            c1, c2 = Chromosome.crossover(p1, p2, self.crossover_probability)
            c1.intra_depot_mutation(self.intra_depot_probability)
            c2.intra_depot_mutation(self.intra_depot_probability)
            c1.inter_depot_mutation(self.inter_depot_probability)
            c2.inter_depot_mutation(self.inter_depot_probability)
            new_population.extend([c1, c2])
        self.population = new_population
        self.print_summary()

    def print_summary(self):
        best = self.get_fittest(self.population, 1)[0]
        print("fitness:", best.calculate_fitness())
        print("distance:", best.calculate_distance())
        print("excess load:", best.calculate_excess_load())

    @staticmethod
    def get_fittest(individuals: list, number: int) -> list:
        assert number <= len(individuals)
        fitness_sorted = sorted(individuals, key=lambda x: x.calculate_fitness(), reverse=True)
        return fitness_sorted[0:number]
