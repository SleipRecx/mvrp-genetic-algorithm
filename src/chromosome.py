import numpy as np
from typing import Dict


class Chromosome:
    def __init__(self, problem):
        self.customers = problem.customers
        self.depots = problem.depots
        self.routes = {}
        self.initial_cluster = self.get_initial_cluster()
        print(self.initial_cluster)
        for depot in self.depots:
            self.routes[depot[0]] = []

    def get_initial_cluster(self) -> Dict:
        cluster = {}
        for customer in self.customers:
            best_distance = float('inf')
            best_depot = None
            for depot in self.depots:
                distance = np.linalg.norm(customer[1:3] - depot[1:3])
                if distance < best_distance:
                    best_depot = depot[0]
                    best_distance = distance
            cluster[customer[0]] = best_depot
        return cluster
