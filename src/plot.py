import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from collections import defaultdict
from util import read_problem_file


def plot(filename, filepath) -> None:
    plt.clf()
    customers, depots, max_vehicle = read_problem_file("../data/problem/" + filename.split("-")[0])
    distance, routes = read_results_file(filename)
    distance = round(float(distance), 7)

    plt.title("Distance = " + str(distance))

    for customer_id in customers:
        x = customers[customer_id][0][0]
        y = customers[customer_id][0][1]
        plt.scatter(x, y, color='black', s=15, zorder=3)

    for depot_id in depots:
        x_depot = depots[depot_id][0][0]
        y_depot = depots[depot_id][0][1]
        plt.plot(x_depot, y_depot, color='red', marker="s", zorder=2)

        for i, route in enumerate(routes[depot_id]):
            route = [int(customer) for customer in route if customer != 0]
            route = [x for x in route if x != 0]

            x_cords = list(map(lambda e: customers[e][0][0], route))
            y_cords = list(map(lambda e: customers[e][0][1], route))
            x_cords.append(x_depot)
            y_cords.append(y_depot)
            x_cords.insert(0, x_depot)
            y_cords.insert(0, y_depot)
            plt.plot(x_cords, y_cords, zorder=1)

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5,
                   handles=[mpatches.Patch(color='black', label=str(len(customers)) + ' Customers'),
                            mpatches.Patch(color='red', label=str(len(depots)) + ' Depots')])

    plt.show()


def read_results_file(filename):
    file_path = "../data/our_solution/" + filename
    file = open(file_path, "r")
    distance = file.readline().strip()
    routes = defaultdict(list)
    for line in file:
        depot_id = int(line.split()[0])
        route = line.split()[4:]
        routes[depot_id].append(route)

    return distance, routes


if __name__ == '__main__':
    path = "../data/our_solution/"
    filenames = sorted(os.listdir("../data/our_solution/"), key=lambda x: os.path.getctime(path+x), reverse=True)
    for i, file in enumerate(filenames):
        print(i + 1, file)

    selection = int(input("Select the file number you would like to plot: "))
    filename = filenames[selection - 1]
    print("FILE", filename)
    plot(filename, path)
