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
        self.row_nets = set()   # set of nets that are part of this row
        self.lower_left_corner = Point(x_min, y_min)
        self.lower_right_corner = Point(x_max, y_min)
        self.upper_left_corner = Point(x_min, y_max)
        self.upper_right_corner = Point(x_max, y_max)
        self.density = None

    def append_node(self, node):
        if node.node_type == "Non_Terminal":
            self.row_nodes.append(node)

    def append_net(self, net):
        self.row_nets.add(net)

    def calculate_row_density(self):
        nodes_area = 0
        row_area = (self.x_max - self.x_min) * (self.y_max - self.y_min)
        for node in self.row_nodes:
            nodes_area += (node.node_height * node.node_width)

        self.density = int((nodes_area / row_area) * 100)

    def display_row_nets(self):
        print("\nNet(s) of " + str(self.row_name) + ":")
        for net in self.row_nets:
            print(net.net_name, end=" ")

    def display_row_nodes(self):
        print("\nNode(s) of " + str(self.row_name) + ":")
        for node in self.row_nodes:
            print(node.node_name + " " + node.node_type, end=" ")

    def display_row_density(self):
        print("\n" + str(self.row_name) + " has density = "
              + str(self.density) + "%")

    def __str__(self):
        return (str(self.row_name) + " - y_min: "
                + str(self.y_min) + " - y_max: "
                + str(self.y_max) + " - x_min: "
                + str(self.x_min) + " - x_max: " + str(self.x_max))