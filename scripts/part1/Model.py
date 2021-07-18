import matplotlib.pyplot as plt
from matplotlib import patches

from scripts import functions


class Model:
    # change to appropriate path. If the path is not needed it can be left blank ("")
    node_list, row_list = functions.parser("../../docs/designs/design/")
    # extract rows
    rows = row_list.__len__()

    figure = plt.figure()
    figure.suptitle("modeling")
    # gs = GridSpec(rows, 1, figure)
    ax = figure.add_subplot()

    row_number = 1
    # x = [0, 10, 20, 30, 40]
    # y = [0, 0, 0, 0, 0]  # starting point

    for row in row_list:
        x = [row.lower_left_x_coordinate, row.lower_right_x_coordinate]
        y = [row.lower_left_y_coordinate, row.lower_left_y_coordinate]
        # temporary_y = np.array(y)
        # y_with_height = temporary_y + row.row_height  # add each element in list by number.
        ax.plot(x, y, label="row {}".format(row_number))
        # y = y_with_height
        row_number += 1

    for node in node_list:
        if node.node_type == "Non_Terminal":
            # TODO node_x and node_y is not rdy
            # node_x = [node.node_x, node.node_x, node.node_x + node.node_width, node.node_x + node.node_width]
            # node_y = [node.node_y, node.node_y, node.node_y + node.node_height, node.node_y + node.node_height]
            node_x = [node.node_x, node.node_x, node.node_x + node.node_width, node.node_x + node.node_width]
            node_y = [node.node_y, node.node_y + node.node_height, node.node_y + node.node_height, node.node_y]
            print(node_x)
            print(node_y)
            ax.add_patch(patches.Polygon(xy=list(zip(node_x, node_y)), fill=False))

    plt.show()
    # TODO add row height, x lower left coordinate ,x lower right coordinate
    # and lower left corner y coordinate
    # for row in range(rows):
    #     ax = figure.add_subplot(gs[row, :])

    # ax1 = figure.add_subplot(111, aspect='equal')
    # ax = plt.axes()
    # TODO
    # Parallelogram
    # x = [0.5, 0.5, 0.5, 0.5]
    # y = [0.5, 0.5, 0.5, 0.5]
    # ax.add_patch(patches.Polygon(xy=list(zip(x, y)), fill=False))

    # display final result
