# TODO add comments

from scripts.classes.Node import Node


def total_calculate_net_wirelength(net_list: list) -> int:
    wirelength = 0
    for net in net_list:
        wirelength += net.wirelength
    return wirelength


class Net:

    def __init__(self, net_name, net_degree):
        self.net_name = net_name
        self.net_degree = net_degree
        self.net_nodes = []  # list of nodes for the current net
        self.net_rows = []  # list of rows that this net belongs to
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None
        self.wirelength = None
        self.net_size = None
        self.internal_nodes = []
        self.external_nodes = set()

    def append_node(self, node):
        self.net_nodes.append(node)

    def append_row(self, row):
        self.net_rows.append(row)

    def find_coordinates_of_net(self):
        start = 0
        temp_internal_node_0 = Node(None, None, None, None)
        temp_internal_node_1 = Node(None, None, None, None)
        temp_internal_node_2 = Node(None, None, None, None)
        temp_internal_node_3 = Node(None, None, None, None)

        for node in self.net_nodes:
            start += 1

            if start == 1 and node.node_type == "Non_Terminal":
                self.x_min = node.lower_left_corner.x
                self.x_max = node.lower_right_corner.x
                self.y_min = node.lower_left_corner.y
                self.y_max = node.upper_right_corner.y

                temp_internal_node_0 = node
                temp_internal_node_1 = node
                temp_internal_node_2 = node
                temp_internal_node_3 = node

            elif start == 1 and node.node_type == "Terminal":
                self.x_min = node.node_x
                self.x_max = node.node_x
                self.y_min = node.node_y
                self.y_max = node.node_y

                temp_internal_node_0 = node
                temp_internal_node_1 = node
                temp_internal_node_2 = node
                temp_internal_node_3 = node

            else:
                if node.node_type == "Non_Terminal":
                    if node.lower_left_corner.x < self.x_min:
                        self.x_min = node.lower_left_corner.x
                        temp_internal_node_0 = node
                    if node.lower_right_corner.x > self.x_max:
                        self.x_max = node.lower_right_corner.x
                        temp_internal_node_1 = node
                    if node.lower_left_corner.y < self.y_min:
                        self.y_min = node.lower_left_corner.y
                        temp_internal_node_2 = node
                    if node.upper_right_corner.y > self.y_max:
                        self.y_max = node.upper_right_corner.y
                        temp_internal_node_3 = node
                else:
                    if node.node_x < self.x_min:
                        self.x_min = node.node_x
                        temp_internal_node_0 = node
                    if node.node_x > self.x_max:
                        self.x_max = node.node_x
                        temp_internal_node_1 = node
                    if node.node_y < self.y_min:
                        self.y_min = node.node_y
                        temp_internal_node_2 = node
                    if node.node_y > self.y_max:
                        self.y_max = node.node_y
                        temp_internal_node_3 = node

        for node in self.net_nodes:
            if (node != temp_internal_node_0 and node != temp_internal_node_1
                    and node != temp_internal_node_2
                    and node != temp_internal_node_3):
                self.internal_nodes.append(node)
            else:
                self.external_nodes.add(node)

    def calculate_net_wirelength(self):
        self.wirelength = (self.x_max - self.x_min) + (self.y_max - self.y_min)

    def calculate_net_size(self):
        self.net_size = (self.x_max - self.x_min) * (self.y_max - self.y_min)

    def display_net_nodes(self):
        print("\n" + str(self.net_name)
              + " has net_degree =  " + str(self.net_degree))
        print("Node(s) of this net: ")
        for node in self.net_nodes:
            print(node.node_name, end=" ")

    def display_net_internal_nodes(self):
        print("\nInternal Node(s) of " + str(self.net_name) + ":")
        if self.internal_nodes:
            for node in self.internal_nodes:
                print(node.node_name)
        else:
            print("None")

    def display_net_external_nodes(self):
        print("\nExternal Node(s) of " + str(self.net_name) + ":")
        for node in self.external_nodes:
            print(node.node_name)

    def display_net_rows(self):
        print("\nRow(s) of " + str(self.net_name) + ":")
        for row in self.net_rows:
            print(row.row_name, end=" ")

    def display_net_size(self):
        print(str(self.net_name) + " size = " + str(self.net_size))

    def display_net_wirelength(self):
        print(str(self.net_name) + " wirelength = " + str(self.wirelength))

    def to_dict(self):
        return {
            'Net_name': self.net_name,
            'Nodes': [node.node_name for node in self.net_nodes],
            'Rows': [row.row_name for row in self.net_rows],
            'Internal_nodes': [node.node_name for node in self.internal_nodes],
            'External_nodes': [node.node_name for node in self.external_nodes],
            'x_min': self.x_min,
            'x_max': self.x_max,
            'y_min': self.y_min,
            'y_max': self.y_max,
            # 'list_Half_Perimeter_Wirelength': self.wirelength,
            # 'list_Net_size': self.net_size,
        }

    # not displaying the nodes that are part of the net
    def __str__(self):
        return str(self.net_name) + " " + str(self.net_degree)
