import numpy as np
import random
from copy import deepcopy
from collections import defaultdict
from typing import Dict
from pprint import pprint
from src.util import read_problem_file, plot


class Chromosome:
    def __init__(self, customers, depots, max_vehicles):
        self.customers = customers
        self.depots = depots
        self.max_vehicles = max_vehicles
        self.routes = self.generate_random_routes()

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

    # TODO: add cars without customers to route (maybe)
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

    def calculate_fitness(self):
        distance = 0
        load_exceeded_count = 0
        for depot_id, routes in self.routes.items():
            depot_coordinate = self.depots[depot_id][0]
            for route in routes:
                demand = sum(list(map(lambda x: self.customers[x][2], route)))
                if demand > self.depots[depot_id][2]:
                    load_exceeded_count += 1
                trip = list(map(lambda x: self.customers[x][0], route))
                trip.append(depot_coordinate)
                trip.insert(0, depot_coordinate)
                for i in range(len(trip) - 1):
                    distance += np.linalg.norm(trip[i] - trip[i + 1])
        return (1 / (distance + 1 * (load_exceeded_count + 1))) * 1000


if __name__ == '__main__':
    c, d, m = read_problem_file("../data/problem/p01")
    solution = Chromosome(c, d, m)
    plot(solution)
