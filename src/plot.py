# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
#
#
# def plot(solution) -> None:
#     plt.clf()
#     customers = solution.customers
#     depots = solution.depots
#     routes = solution.routes
#
#     plt.title("Distance = " + str(round(solution.calculate_distance(), 7)))
#
#     for customer_id in customers:
#         x = customers[customer_id][0][0]
#         y = customers[customer_id][0][1]
#         plt.scatter(x, y, color='blue', zorder=3)
#
#     for depot_id in depots:
#         x_depot = depots[depot_id][0][0]
#         y_depot = depots[depot_id][0][1]
#
#         plt.plot(x_depot, y_depot, color='red', marker="s", zorder=2)
#
#         for route in routes[depot_id]:
#             x_cords = list(map(lambda e: customers[e][0][0], route))
#             y_cords = list(map(lambda e: customers[e][0][1], route))
#             x_cords.append(x_depot)
#             y_cords.append(y_depot)
#             x_cords.insert(0, x_depot)
#             y_cords.insert(0, y_depot)
#             plt.plot(x_cords, y_cords, zorder=1)
#     plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5,
#                handles=[mpatches.Patch(color='blue', label=str(len(customers)) + ' Customers'),
#                         mpatches.Patch(color='red', label=str(len(depots)) + ' Depots')])
#     plt.pause(0.001)
