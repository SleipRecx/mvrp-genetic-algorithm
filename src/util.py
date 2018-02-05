from typing import Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def parse_problem(filename: str) -> Tuple:
    file = open(filename, "r")
    line1 = list(map(lambda e: int(e), file.readline().split()))
    number_of_vehicles = line1[0]
    number_of_customers = line1[1]
    number_of_depots = line1[2]
    depots = []
    customers = []
    for i in range(number_of_depots):
        depots.append(list(map(lambda e: int(e), file.readline().split())))
    for i in range(number_of_customers):
        customers.append(list(map(lambda e: int(e), file.readline().split())))
    for i in range(number_of_depots):
        depots[i].extend(list(map(lambda e: int(e), file.readline().split())))
    return customers, depots, number_of_vehicles


def plot_problem(data):
    customers = data[0]
    depots = data[1]
    number_of_vehicles = data[2]

    for c in customers:
        x = c[1]
        y = c[2]
        plt.scatter(x, y, color='blue')

    for d in depots:
        x = d[3]
        y = d[4]
        plt.scatter(x, y, color='red', s=200)
        for i in range(number_of_vehicles):
            plt.scatter(x, y, color='yellow')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5,
               handles=[mpatches.Patch(color='blue', label='Customers'), mpatches.Patch(color='red', label='Depots'),
                        mpatches.Patch(color='yellow', label='Vehicles')])
    plt.show()


if __name__ == '__main__':
    problem = parse_problem("../data/problem/p01")
    plot_problem(problem)
