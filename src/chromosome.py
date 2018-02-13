import random
from copy import deepcopy
from collections import defaultdict
from typing import Dict, Tuple
from src.util import copy_dict, euclidean_distance


def put_in_least_cost_place(chromosome, route, depot_id):
    for crossover_customer_id in route:
        best_customer_to_follow = [None, float('inf')]
        crossover_customer_coordinates = (chromosome.customers[crossover_customer_id][0][0],
                                          chromosome.customers[crossover_customer_id][0][1])

        for route_index, route in enumerate(chromosome.routes[depot_id]):
            if len(route) > 0:
                for customer_index, route_customer_id in enumerate(route):
                    route_customer_coordinates = (chromosome.customers[route_customer_id][0][0],
                                                  chromosome.customers[route_customer_id][0][1])

                    distance = euclidean_distance(crossover_customer_coordinates, route_customer_coordinates)
                    if distance < best_customer_to_follow[1]:
                        best_customer_to_follow = [route_customer_id, distance, [route_index, customer_index]]
            else:
                depot_coordinates = (chromosome.depots[depot_id][0][0], chromosome.depots[depot_id][0][1])

                distance_to_depot = euclidean_distance(crossover_customer_coordinates, depot_coordinates)
                if distance_to_depot < best_customer_to_follow[1]:
                    best_customer_to_follow = [0, distance_to_depot, [route_index, 0]]

        chromosome.routes[depot_id][best_customer_to_follow[2][0]].insert(best_customer_to_follow[2][1] + 1,
                                                                          crossover_customer_id)

    return chromosome


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

        c1.routes = copy_dict(p1.routes)
        c2.routes = copy_dict(p2.routes)

        depot_id = random.choice(list(c1.depots.keys()))

        c1_route = random.choice(c1.routes[depot_id])
        c2_route = random.choice(c2.routes[depot_id])

        for _, routes in c1.routes.items():
            for i in range(len(routes)):
                routes[i] = [x for x in routes[i] if x not in c2_route]

        for _, routes in c2.routes.items():
            for i in range(len(routes)):
                routes[i] = [x for x in routes[i] if x not in c1_route]

        c1 = put_in_least_cost_place(c1, c2_route, depot_id)
        c2 = put_in_least_cost_place(c2, c1_route, depot_id)

        return c1, c2

    def mutation(self):
        self._intra_depot_mutation(0.9)
        self._inter_depot_mutation(0.3)

    def _intra_depot_mutation(self, probability: float = 0.8):
        def swapping() -> None:
            depot_id = random.choice(list(self.depots.keys()))
            route1 = random.choice(self.routes[depot_id])
            if len(route1) > 0:
                route2 = random.choice(self.routes[depot_id])
                customer = random.choice(route1)
                route1.remove(customer)
                position = random.randint(0, len(route2))
                route2.insert(position, customer)

        def route_reversal() -> None:
            depot_id = random.choice(list(self.depots.keys()))
            route = random.choice(self.routes[depot_id])
            if len(route) > 0:
                points = [random.randint(0, len(route)), random.randint(0, len(route))]
                points.sort()
                route[points[0]:points[1]] = list(reversed(route[points[0]:points[1]]))

        mutate = random.choice([route_reversal, swapping])
        if random.random() < probability:
            mutate()

    def _inter_depot_mutation(self, probability: float = 0.1) -> None:
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
                key = str(depot_id) + str(route)
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
        return 1 / (self.calculate_distance() * (load + 1)) * 1000
