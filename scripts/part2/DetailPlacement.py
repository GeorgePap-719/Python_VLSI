from natsort import *

from scripts.classes.Net import total_calculate_net_wirelength
from scripts.classes.Node import Node
from scripts.part1.Legalization import update_net_list


def first_detailed_placement(node_list: list, row_list: list, net_list: list):
    updated_net_list: list = net_list
    for row in row_list:
        changes_flag = True

        # we stop only when there are no more changes that lead to better result
        while changes_flag:
            changes_flag = False
            """ Sort the given iterable in the way that humans expect."""
            sorted_list: list[Node] = natsorted(row.row_nodes, key=lambda x: natsort_key(x.node_name))
            for index, node in enumerate(sorted_list):
                if index + 1 == len(sorted_list):
                    break
                for index2, node2 in enumerate(sorted_list):
                    if index2 + 1 == len(sorted_list):
                        continue
                    if index2 == index:
                        continue
                    if node.node_width == node2.node_width:
                        wirelength = total_calculate_net_wirelength(net_list)
                        swap_positions(sorted_list, index, index2)
                        updated_net_list = update_net_list(net_list, node_list)
                        print("wirelength")
                        new_wirelength = total_calculate_net_wirelength(updated_net_list)
                        if new_wirelength > wirelength:
                            changes_flag = True
                            break  # make the first advantageous exchange
                        else:
                            # swap back positions
                            swap_positions(sorted_list, index2, index)

    return node_list, row_list, updated_net_list


def swap_positions(data_list: list, position1: int, position2: int):
    data_list[position1], data_list[position2] = data_list[position2], data_list[position1]
