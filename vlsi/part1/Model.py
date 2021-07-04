import matplotlib.patches as patches
import matplotlib.pyplot as plt

from vlsi import functions


class Model:

    # TODO def __init__(self):

    @staticmethod
    def modeling():
        stat = 1

    # change to appropriate path. If the path is not needed it can be left blank ("")
    node_list, row_list = functions.parser("../../docs/designs/design/")

    # for node in node_list:
    # print(" the node list is {}".format(node))
    # print("row: {}".format(node.node_row))
    # print(node.node_row)

    for row in row_list:
        print(row_list.__len__())
    # create rows


figure = plt.figure()
ax = figure.add_subplot(111, aspect='equal')
# ax = plt.axes()

# TODO
# Parallelogram
# x = [0.5, 0.6, .7, .4]
# y = [0.4, 0.4, 0.6, 0.6]
x = [0.5, 0.5, 0.5, 0.5]
y = [0.5, 0.5, 0.5, 0.5]
ax.add_patch(patches.Polygon(xy=list(zip(x, y)), fill=False))

plt.show()
