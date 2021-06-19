# TODO add comments
class Net:

    def __init__(self, net_name, net_degree):
        self.net_name = net_name
        self.net_degree = net_degree
        self.net_nodes = []  # list of nodes for the current net
        self.net_rows = []  # list of rows that this net belongs to # TODO on parser()
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None
        self.wire_length = None
        self.net_size = None

    # update the list of nodes of this net
    def append_node(self, node):
        self.net_nodes.append(node)

    def find_coordinates_of_net(self):
        start = 0
        for node in self.net_nodes:
            start += 1

            if start == 1 and node.node_type == "Non_Terminal":
                self.x_min = node.lower_left_corner.x
                self.x_max = node.lower_right_corner.x
                self.y_min = node.lower_left_corner.y
                self.y_max = node.upper_right_corner.y
            elif start == 1 and node.node_type == "Terminal":
                self.x_min = node.node_x
                self.x_max = node.node_x
                self.y_min = node.node_y
                self.y_max = node.node_y
            else:
                if node.node_type == "Non_Terminal":
                    if node.lower_left_corner.x < self.x_min:
                        self.x_min = node.lower_left_corner.x
                    if node.lower_right_corner.x > self.x_max:
                        self.x_max = node.lower_right_corner.x
                    if node.lower_left_corner.y < self.y_min:
                        self.y_min = node.lower_left_corner.y
                    if node.upper_right_corner.y > self.y_max:
                        self.y_max = node.upper_right_corner.y
                else:
                    if node.node_x < self.x_min:
                        self.x_min = node.node_x
                    if node.node_x > self.x_max:
                        self.x_max = node.node_x
                    if node.node_y < self.y_min:
                        self.y_min = node.node_y
                    if node.node_y > self.y_max:
                        self.y_max = node.node_y

    def calculate_net_wire_length(self):
        self.wire_length = (self.x_max - self.x_min) + (self.y_max - self.y_min)

    def calculate_net_size(self):
        self.net_size = (self.x_max - self.x_min) * (self.y_max - self.y_min)

    def display_net(self):
        print("\n" + str(self.net_name)
              + " - netDegree =  " + str(self.net_degree))
        print("Nodes of this net: ")
        for node in self.net_nodes:
            print(node.node_name, end=" ")

    def display_net_size(self):
        print(str(self.net_name) + " size = " + str(self.net_size))

    def display_net_wire_length(self):
        print(str(self.net_name) + " wire_length = " + str(self.wire_length))

    # not displaying the nodes that are part of the net
    def __str__(self):
        return str(self.net_name) + " " + str(self.net_degree)
