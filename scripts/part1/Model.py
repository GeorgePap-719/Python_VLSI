import matplotlib.pyplot as plt
from matplotlib import patches

from scripts.classes.Node import Node
from scripts.classes.Point import Point
from scripts.classes.Row import Row


def to_point():
    print("TODO")


def do_overlap(node1: Node, node2: Node) -> bool:
    if node1.node_type == "Non_Terminal" and node2.node_type == "Non_Terminal":
        l1: Point = Point(node1.node_x, node1.node_x + node1.node_width)
        r1: Point = Point(node1.node_y, node1.node_y + node1.node_height)
        l2: Point = Point(node2.node_x, node2.node_x + node2.node_width)
        r2: Point = Point(node2.node_y, node2.node_y + node2.node_height)
        return Point.do_overlap(l1, r1, l2, r2)
    else:
        return False


def count_overlaps_in_row(row: Row) -> int:
    node_list = row.row_nodes
    counter = 0

    for node1 in node_list:
        for node2 in node_list:
            if node1 == node2:
                continue
        if do_overlap(node1, node2):
            counter += 1

    return counter


def count_overlaps_in_row_list(row_list: list) -> int:
    counter = 0

    for row in row_list:
        counter += count_overlaps_in_row(row)

    return counter


# TODO change name of class, maybe drop class object.
def modeling(node_list: list, row_list: list, net_list: list):
    figure = plt.figure()
    figure.suptitle("modeling")
    ax = figure.add_subplot()
    row_number = 1

    # TODO if there is enough time and will create function to return random colors in hex
    colors = ['#caa24e', '#caa24e', '#5a3e42', '#b35031', '#5a3e42', '#6e6e64', '#8f050e', '#e3ce82']
    number_of_colors = 0

    for row in row_list:
        x = [row.lower_left_x_coordinate, row.lower_right_x_coordinate]
        y = [row.lower_left_y_coordinate, row.lower_left_y_coordinate]
        ax.plot(x, y, label="row {}".format(row_number))
        row_number += 1

    number_of_nodes = 1
    polygons = {}
    for node in node_list:
        if node.node_type != "Non_Terminal":
            x = [node.node_x + node.node_width]
            y = [node.node_y + node.node_height]
            ax.plot(x, y, "o", markersize=10)
        if node.node_type == "Non_Terminal":
            node_x = [node.node_x, node.node_x, node.node_x + node.node_width, node.node_x + node.node_width]
            node_y = [node.node_y, node.node_y + node.node_height, node.node_y + node.node_height, node.node_y]
            # we dont have unique colors for each cell.
            ax.add_patch(
                patches.Polygon(xy=list(zip(node_x, node_y)), fill=True, color=colors[number_of_colors],
                                label=number_of_nodes))
        if number_of_colors == 7:
            number_of_colors = 0
        number_of_colors += 1
        number_of_nodes += 1

    for net in net_list:
        net_x = [net.x_min, net.x_min, net.x_max, net.x_max]
        net_y = [net.y_min, net.y_max, net.y_max, net.y_min]
        ax.add_patch(patches.Polygon(xy=list(zip(net_x, net_y)), fill=False, linestyle="dashed"))

    # TODO add labels in cells
    # ax = plt.subplots
    # for poly in polygons:
    #     print(poly)
    #     # print(current_patch)
    #     # cx = rx + (node.node_x + node.node_width) / 2.0
    #     # cy = ry + (node.node_y + node.node_height) / 2.0
    #     # ax.annotate(patches, (cx, cy), weight='bold', fontsize=5, ha='center', va='center')

    # display final result
    plt.show()
