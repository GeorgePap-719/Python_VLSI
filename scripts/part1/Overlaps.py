from scripts.classes.Node import Node
from scripts.classes.Point import Point
from scripts.classes.Row import Row


def simple_do_overlap(node1: Node, node2: Node) -> bool:
    if node1.node_type == "Non_Terminal" and node2.node_type == "Non_Terminal":

        # If one rectangle is on left side of other
        if node1.node_x >= node2.node_x + node2.node_width or \
                node1.node_x + node1.node_width <= node2.node_x:
            return False

        # if node1.node_x + node1.node_width <= node2.node_x or \
        #         node2.node_x + node2.node_width <= node1.node_x:
        #     return False

        return True

    else:
        return False


def do_overlap(l1, r1, l2, r2) -> bool:
    """Returns true if two rectangles(l1, r1)
           and (l2, r2) overlap  """

    # To check if either rectangle is actually a line
    # For example  :  l1 ={-1,0}  r1={1,1}  l2={0,-1}  r2={0,1}
    # if l1.x == r1.x or l1.y == r1.y or l2.x == r2.x or l2.y == r2.y:
    # the line cannot have positive overlap
    # return False

    # If one rectangle is on left side of other
    if l1.x >= r2.x or l2.x >= r1.x:
        return False

    # This does suit as in our case
    # If one rectangle is above other
    # if r1.y >= l2.y or r2.y >= l1.y:
    #     return False

    return True


def complex_do_overlap(node1: Node, node2: Node) -> bool:
    if node1.node_type == "Non_Terminal" and node2.node_type == "Non_Terminal":
        l1: Point = Point(node1.node_x, node1.node_x + node1.node_width)
        r1: Point = Point(node1.node_y, node1.node_y + node1.node_height)
        l2: Point = Point(node2.node_x, node2.node_x + node2.node_width)
        r2: Point = Point(node2.node_y, node2.node_y + node2.node_height)
        return do_overlap(l1, r1, l2, r2)
    else:
        return False


def count_overlaps_in_row(row: Row) -> int:
    node_list = row.row_nodes

    counter = 0
    for index, node1 in enumerate(node_list):
        for index2, node2 in enumerate(node_list):
            index2 += index
            if node1 == node2:
                continue
            if simple_do_overlap(node1, node2):
                counter += 1

    return counter


def count_overlaps_in_row_simple(row: Row) -> int:
    node_list = row.row_nodes
    counter = 0

    for index, node1 in enumerate(node_list):
        if index + 1 != len(node_list):
            if simple_do_overlap(node1, node_list[index + 1]):
                counter += 1

    return counter


def count_overlaps_in_row_list(row_list: list) -> int:
    counter = 0

    for row in row_list:
        counter += count_overlaps_in_row_simple(row)

    return counter
