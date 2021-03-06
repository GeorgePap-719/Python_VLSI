# TODO add comments

class Row:

    def __init__(self, row_name=None, y_min=None, y_max=None, x_min=None, x_max=None,
                 number_of_rows=None, lower_left_y_coordinate=None, row_height=None,
                 lower_left_x_coordinate=None, lower_right_x_coordinate=None):
        self.number_of_rows = number_of_rows
        self.lower_left_y_coordinate = lower_left_y_coordinate
        self.row_height = row_height
        self.lower_left_x_coordinate = lower_left_x_coordinate
        self.lower_right_x_coordinate = lower_right_x_coordinate
        self.row_name = row_name
        self.y_min = y_min
        self.y_max = y_max
        self.x_min = x_min
        self.x_max = x_max
        self.row_nodes = []  # list of nodes that are placed in this row
        self.row_nets = set()  # set of nets that are part of this row

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

    def to_dict(self):
        return {
            'Row_name': self.row_name,
            'Cells': [node.node_name for node in self.row_nodes],
            'Nets': [net.net_name for net in self.row_nets],
            'Coordinate_x_min': self.x_min,
            'Coordinate_x_max': self.x_max,
            'Coordinate_y_min': self.y_min,
            'Coordinate_y_max': self.y_max,
        }

    def __str__(self):
        return (str(self.row_name) + " - y_min: "
                + str(self.y_min) + " - y_max: "
                + str(self.y_max) + " - x_min: "
                + str(self.x_min) + " - x_max: " + str(self.x_max))
