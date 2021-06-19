# TODO add comments
from vlsi.classes.Point import Point


class Row:

    def __init__(self, row_name, y_min, y_max, x_min, x_max):
        self.row_name = row_name
        self.y_min = y_min
        self.y_max = y_max
        self.x_min = x_min
        self.x_max = x_max
        self.row_nodes = []  # list of nodes that are placed in this row
        self.row_nets = []  # list of nets that are part of this row # TODO on parser()
        self.lower_left_corner = Point(x_min, y_min)
        self.lower_right_corner = Point(x_max, y_min)
        self.upper_left_corner = Point(x_min, y_max)
        self.upper_right_corner = Point(x_max, y_max)

    # update the list of nodes of this row
    def append_node(self, node):
        if node.node_type == "Terminal":
            pass
        else:
            self.row_nodes.append(node)

    # update the list of nets of this row
    def append_net(self, net):  # TODO on parser()
        self.row_nets.append(net)

    # display row name and nodes of this row
    def display_row(self):
        print("\n" + str(self.row_name))
        print("Nodes of this row: ")
        for i in self.row_nodes:
            print(i, end=" ")

    def __str__(self):
        return (str(self.row_name) + " - y_min: "
                + str(self.y_min) + " - y_max: "
                + str(self.y_max) + " - x_min: "
                + str(self.x_min) + " - x_max: " + str(self.x_max))
