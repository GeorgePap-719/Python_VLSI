import matplotlib.pyplot as plt
import numpy as np

from scripts import functions


class Model:
    # change to appropriate path. If the path is not needed it can be left blank ("")
    node_list, row_list = functions.parser("../../docs/designs/design/")
    # extract rows
    rows = row_list.__len__()

    figure = plt.figure()

    figure.suptitle("modeling")
    # gs = GridSpec(rows, 1, figure)

    row_number = 1
    x = [10, 20, 30, 40, 50]
    y = [0, 0, 0, 0, 0]  # starting point

    for row in row_list:
        temporary_y = np.array(y)
        y_with_height = temporary_y + row.row_height  # add each element in list by number.
        y = y_with_height
        plt.plot(x, y_with_height, label="row {}".format(row_number))
        row_number += 1

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
