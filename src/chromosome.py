import numpy as np
import random
from copy import deepcopy
from collections import defaultdict
from pprint import pprint
from typing import Dict, Tuple
from src.util import read_problem_file


class Chromosome:
    route_memo = {}
    load_memo = {}

    def __init__(self, customers, depots, max_vehicles, init_routes: bool = True):
        self.customers = customers
        self.depots = depots
        self.max_vehicles = max_vehicles
        self.routes = {}
        if init_routes:
            self.routes = self.generate_random_routes()

    @classmethod
    def crossover(cls, p1, p2) -> Tuple:
        c1 = cls(p1.customers, p1.depots, p1.max_vehicles, False)
        c2 = cls(p2.customers, p2.depots, p2.max_vehicles, False)

        c1.routes = deepcopy(p1.routes)
        c2.routes = deepcopy(p2.routes)

        if random.random() > 0.2:  # TODO: remember
            return c1, c2

        depot_id = random.choice(list(c1.depots.keys()))

        c1_route = random.choice(c1.routes[depot_id])
        c2_route = random.choice(c2.routes[depot_id])

        for _, routes in c1.routes.items():
            for i in range(len(routes)):
                routes[i] = [x for x in routes[i] if x not in c2_route]

        for _, routes in c2.routes.items():
            for i in range(len(routes)):
                routes[i] = [x for x in routes[i] if x not in c1_route]

        for number in c2_route:
            route = random.choice(c1.routes[depot_id])
            route.insert(random.randint(0, len(route)), number)

        for number in c1_route:
            route = random.choice(c2.routes[depot_id])
            route.insert(random.randint(0, len(route)), number)
        return c1, c2

    def intra_depot_mutation(self, probability: float = 0.8):
        def swapping() -> None:
            depot_id = random.choice(list(self.depots.keys()))
            route1 = random.choice(list(filter(lambda x: len(x) > 0, self.routes[depot_id])))
            route2 = random.choice(self.routes[depot_id])
            customer = random.choice(route1)
            route1.remove(customer)
            position = random.randint(0, len(route2))
            route2.insert(position, customer)

        def route_reversal() -> None:
            depot_id = random.choice(list(self.depots.keys()))
            route = random.choice(list(filter(lambda x: len(x) > 0, self.routes[depot_id])))
            points = [random.randint(0, len(route)), random.randint(0, len(route))]
            points.sort()
            route[points[0]:points[1]] = list(reversed(route[points[0]:points[1]]))

        mutate = random.choice([route_reversal, swapping])
        if random.random() < probability:
            mutate()

    # TODO: Implement
    def inter_depot_mutation(self):
        pass

    def get_customer_cluster(self) -> Dict:
        cluster = defaultdict(list)
        for customer_id in self.customers:
            customer_coordinate = self.customers[customer_id][0]
            best_distance = float('inf')
            best_depot = None
            for depot_id in self.depots:
                depot_coordinate = self.depots[depot_id][0]
                distance = np.linalg.norm(customer_coordinate - depot_coordinate)
                if distance < best_distance:
                    best_depot = depot_id
                    best_distance = distance
            cluster[best_depot].append(customer_id)
        return cluster

    def generate_random_routes(self) -> Dict:
        routes = defaultdict(list)
        cluster = self.get_customer_cluster()
        empty_route = [[] for _ in range(self.max_vehicles)]
        for depot_id, customers in cluster.items():
            routes[depot_id] = deepcopy(empty_route)
            for customer_id in customers:
                route_number = random.randint(0, self.max_vehicles - 1)
                routes[depot_id][route_number].append(customer_id)
        return routes

    def calculate_distance(self):
        distance = 0
        for depot_id, routes in self.routes.items():
            depot_coordinate = self.depots[depot_id][0]
            for route in routes:
                key = str(depot_id) + str(route)
                if key in Chromosome.route_memo:
                    distance += Chromosome.route_memo[key]
                else:
                    trip = list(map(lambda x: self.customers[x][0], route))
                    trip.append(depot_coordinate)
                    trip.insert(0, depot_coordinate)
                    route_distance = 0
                    for i in range(len(trip) - 1):
                        route_distance += np.linalg.norm(trip[i] - trip[i + 1])
                    Chromosome.route_memo[key] = route_distance
                    distance += route_distance
        return distance

    def calculate_excess_load(self):
        excess_load = 0
        for depot_id, routes in self.routes.items():
            for route in routes:
                key = str(route)
                if key in Chromosome.load_memo:
                    load = Chromosome.load_memo[key]
                else:
                    load = sum(list(map(lambda x: self.customers[x][2], route)))
                    Chromosome.load_memo[key] = load
                if load > self.depots[depot_id][2]:
                    excess_load += load - self.depots[depot_id][2]
        return excess_load

    def calculate_fitness(self):
        load = self.calculate_excess_load()
        return 1 / (self.calculate_distance() * ((load / 20) + 1)) * 1000


if __name__ == '__main__':
    c, d, m = read_problem_file("../data/problem/p2")
    solution = Chromosome(c, d, m)
