import matplotlib.pyplot as plt
from matplotlib import patches

from scripts import functions


class Model:
    # change to appropriate path. If the path is not needed it can be left blank ("")
    node_list, row_list, net_list = functions.parser("../../docs/designs/design/")

    figure = plt.figure()
    figure.suptitle("modeling")
    ax = figure.add_subplot()
    row_number = 1

    for row in row_list:
        x = [row.lower_left_x_coordinate, row.lower_right_x_coordinate]
        y = [row.lower_left_y_coordinate, row.lower_left_y_coordinate]
        ax.plot(x, y, label="row {}".format(row_number))
        row_number += 1

    for node in node_list:
        if node.node_type != "Non_Terminal":
            x = [node.node_x + node.node_width]
            y = [node.node_y + node.node_height]
            ax.plot(x, y, "o", markersize=10)
        if node.node_type == "Non_Terminal":
            node_x = [node.node_x, node.node_x, node.node_x + node.node_width, node.node_x + node.node_width]
            node_y = [node.node_y, node.node_y + node.node_height, node.node_y + node.node_height, node.node_y]
            ax.add_patch(patches.Polygon(xy=list(zip(node_x, node_y)), fill=False))

    # TODO needs check
    for net in net_list:
        net_x = [net.x_min, net.x_min, net.x_min + net.x_max, net.x_min + net.x_max]
        net_y = [net.y_min, net.y_min + net.y_max, net.y_min + net.y_max, net.y_min]
        ax.add_patch(patches.Polygon(xy=list(zip(net_x, net_y)), fill=False, linestyle="dashed"))

    # display final result
    plt.show()
