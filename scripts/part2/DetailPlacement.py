from natsort import natsort_key

from scripts.classes.Node import Node


def first_detailed_placement(node_list: list, row_list: list, net_list: list):
    for row in row_list:
        # sort list alphabetical-numeric
        # sorted_list: list[Node] = row.row_nodes
        # sorted_list: list[Node] = natsorted(row.row_nodes, key=operator.attrgetter('node_name'))
        # row.row_nodes.sort(key=natural_key())
        # sorted_list: list[Node] = natsorted(row.row_nodes, key=lambda x: (not x.node_name.isdigit(), x.node_name))
        sorted_list: list[Node] = sorted(row.row_nodes,
                                         key=lambda x: (not x.node_name.isdigit(), natsort_key(x.node_name)))
        # sorted_list: list[Node] = sorted(row.row_nodes, key=natural_key)
        # natsort_key = natsort_keygen(key=lambda y: y.node_name)

        for node in sorted_list:
            print(node.node_name)
