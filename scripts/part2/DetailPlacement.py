import operator

from scripts.classes.Node import Node


def first_detailed_placement(node_list: list, row_list: list, net_list: list):
    print("TODO")

    for row in row_list:
        # sort list alphabetical
        sorted_list: list[Node] = sorted(row.row_nodes, key=operator.attrgetter('node_name'))
        print(sorted_list)
