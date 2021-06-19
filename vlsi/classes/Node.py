# TODO add comments

from vlsi.classes.Point import Point
from vlsi.classes.Row import Row


class Node:

    def __init__(self, node_name, node_width, node_height, node_type,
                 node_x=0, node_y=0):
        self.node_name = node_name
        self.node_width = node_width
        self.node_height = node_height
        self.node_type = node_type
        self.node_x = node_x  # Lower Left Corner - x Coordinate
        self.node_y = node_y  # Lower Left Corner - y Coordinate
        self.lower_left_corner = Point(None, None)
        self.lower_right_corner = Point(None, None)
        self.upper_left_corner = Point(None, None)
        self.upper_right_corner = Point(None, None)

        self.node_nets = []  # net_names that this node are part of #TODO net objects
        self.node_row = Row(None, None, None, None, None)  # row that this node is placed in

    # update the Coordinates x & y
    def set_x_y(self, node_x, node_y):
        self.node_x = node_x
        self.node_y = node_y

    def set_row(self, row):
        self.node_row = row

    # update the list of nets
    def append_net(self, net_name):
        self.node_nets.append(str(net_name))

    # calculate the coordinates of the 4-corners of the node
    # Terminals are dots, they do not have corners
    def set_points(self, x_min, x_max, y_min, y_max):
        if self.node_type == "Terminal":
            pass
        else:
            self.lower_left_corner = Point(x_min, y_min)
            self.lower_right_corner = Point(x_max, y_min)
            self.upper_left_corner = Point(x_min, y_max)
            self.upper_right_corner = Point(x_max, y_max)

    def display_node_corners(self):
        print("\nNode name: " + str(self.node_name)
              + "\nLower Left Corner: " + str(self.lower_left_corner)
              + "\nLower Right Corner: " + str(self.lower_right_corner)
              + "\nUpper Left Corner: " + str(self.upper_left_corner)
              + "\nUpper Right Corner: " + str(self.upper_right_corner))

    def display_node_row(self):
        print("\nNode " + str(self.node_name)
              + " is placed in row: " + str(self.node_row.row_name))

    def display_node_nets(self):
        print("\nNode " + str(self.node_name)
              + " belongs to the net(s):  ")
        for i in self.node_nets:
            print(i, end=" ")

    def __str__(self):
        return (str(self.node_name) + " " + str(self.node_width) + " " +
                str(self.node_height) + " " + str(self.node_type) + " " +
                str(self.node_x) + " " + str(self.node_y))
