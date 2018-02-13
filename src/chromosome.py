import random
from copy import deepcopy
from collections import defaultdict
from typing import Dict, Tuple
from util import copy_dict, euclidean_distance


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
    def crossover(cls, p1, p2, probability: float) -> Tuple:
        c1 = cls(p1.customers, p1.depots, p1.max_vehicles, False)
        c2 = cls(p2.customers, p2.depots, p2.max_vehicles, False)
        c1.routes = copy_dict(p1.routes)
        c2.routes = copy_dict(p2.routes)

        if random.random() < probability:
            depot_id = random.choice(list(c1.depots.keys()))

            c1_route = random.choice(c1.routes[depot_id])
            c2_route = random.choice(c2.routes[depot_id])

            for _, routes in c1.routes.items():
                for i in range(len(routes)):
                    routes[i] = [x for x in routes[i] if x not in c2_route]

            for _, routes in c2.routes.items():
                for i in range(len(routes)):
                    routes[i] = [x for x in routes[i] if x not in c1_route]

            for customer in c2_route:
                c1.move_to_best_location(customer)

            for customer in c1_route:
                c2.move_to_best_location(customer)

        return c1, c2

    def intra_depot_mutation(self, probability):
        def swapping():
            depot_id = random.choice(list(self.depots.keys()))
            route1 = random.choice(self.routes[depot_id])
            if len(route1) > 0:
                route2 = random.choice(self.routes[depot_id])
                customer = random.choice(route1)
                route1.remove(customer)
                position = random.randint(0, len(route2))
                route2.insert(position, customer)

        def route_reversal():
            depot_id = random.choice(list(self.depots.keys()))
            route = random.choice(self.routes[depot_id])
            if len(route) > 0:
                points = [random.randint(0, len(route)), random.randint(0, len(route))]
                points.sort()
                route[points[0]:points[1]] = list(reversed(route[points[0]:points[1]]))

        if random.random() < probability:
            random.choice([route_reversal, swapping])()

    def inter_depot_mutation(self, probability):
        if random.random() < probability:
            depot_id = random.choice(list(self.depots.keys()))
            route = random.choice(self.routes[depot_id])
            if len(route) > 0:
                customer = random.choice(route)
                route.remove(customer)
                depot_id = random.choice(self.get_swap_cluster()[customer])
                route = random.choice(self.routes[depot_id])
                route.insert(random.randint(0, len(route)), customer)

    def get_customer_cluster(self) -> Dict:
        cluster = defaultdict(list)
        for customer_id in self.customers:
            customer_coordinate = self.customers[customer_id][0]
            best_distance = float('inf')
            best_depot = None
            for depot_id in self.depots:
                depot_coordinate = self.depots[depot_id][0]
                distance = euclidean_distance(customer_coordinate, depot_coordinate)
                if distance < best_distance:
                    best_depot = depot_id
                    best_distance = distance
            cluster[best_depot].append(customer_id)
        return cluster

    def get_swap_cluster(self) -> Dict:
        cluster = defaultdict(lambda: (int, float("inf")))
        for customer_id in self.customers:
            customer_coordinate = self.customers[customer_id][0]
            for depot_id in self.depots:
                depot_coordinate = self.depots[depot_id][0]
                distance = euclidean_distance(customer_coordinate, depot_coordinate)
                if distance < cluster[customer_id][1]:
                    cluster[customer_id] = depot_id, distance
        swap_cluster = defaultdict(list)
        for customer_id in self.customers:
            customer_coordinate = self.customers[customer_id][0]
            for depot_id in self.depots:
                depot_coordinate = self.depots[depot_id][0]
                distance = euclidean_distance(customer_coordinate, depot_coordinate)
                if ((distance - cluster[customer_id][1]) / cluster[customer_id][1]) <= 2:
                    swap_cluster[customer_id].append(depot_id)
        return swap_cluster

    def generate_random_routes(self) -> Dict:
        routes = defaultdict(list)
        empty_route = [[] for _ in range(self.max_vehicles)]
        for depot_id, customers in self.get_customer_cluster().items():
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
                key = route[:]
                key.append(depot_id)
                key = hash(tuple(key))
                if key in Chromosome.route_memo:
                    distance += Chromosome.route_memo[key]
                else:
                    trip = list(map(lambda x: self.customers[x][0], route))
                    trip.append(depot_coordinate)
                    trip.insert(0, depot_coordinate)
                    route_distance = 0
                    for i in range(len(trip) - 1):
                        route_distance += euclidean_distance(trip[i], trip[i + 1])
                    Chromosome.route_memo[key] = route_distance
                    distance += route_distance
        return distance

    def move_to_best_location(self, customer):
        best = (None, None, None)
        best_score = float("-inf")
        for depot_id, routes in self.routes.items():
            for i in range(0, len(routes)):
                for j in range(0, len(routes[i]) + 1):
                    routes[i].insert(j, customer)
                    fitness = self.calculate_fitness()
                    del routes[i][j]
                    if fitness > best_score:
                        best = depot_id, i, j
                        best_score = fitness
        depot, route, pos = best
        self.routes[depot][route].insert(pos, customer)

    def calculate_excess_load(self):
        excess_load = 0
        for depot_id, routes in self.routes.items():
            for route in routes:
                key = hash(tuple(route))
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
        return 1 / (self.calculate_distance() * (load + 1)) * 1000
