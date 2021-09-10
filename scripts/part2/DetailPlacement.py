import copy

from natsort import *

from scripts.classes.Net import total_calculate_net_wirelength
from scripts.classes.Node import Node
from scripts.part1.Legalization import update_net_list


def first_detailed_placement(node_list: list, row_list: list, net_list: list):
    updated_net_list: list = copy.deepcopy(net_list)
    changes_flag = True
    wirelength = total_calculate_net_wirelength(net_list)

    # we stop only when there are no more changes that lead to better result
    while changes_flag:
        changes_flag = False
        """ Sort the given iterable in the way that humans expect."""
        sorted_list: list[Node] = natsorted(node_list, key=lambda x: natsort_key(x.node_name))
        for index, node in enumerate(sorted_list):
            if index + 1 == len(sorted_list):
                break
            for index2, node2 in enumerate(sorted_list):
                if index2 + 1 == len(sorted_list):
                    continue
                if index2 == index:
                    continue
                if node.node_width == node2.node_width:
                    # swap_positions(sorted_list, index, index2)
                    sorted_list[index], sorted_list[index2] = sorted_list[index2], sorted_list[index]
                    updated_net_list = update_net_list(updated_net_list, node_list)
                    print("wirelength")
                    new_wirelength = total_calculate_net_wirelength(updated_net_list)
                    if new_wirelength > wirelength:
                        print("found better wirelength")
                        wirelength = new_wirelength
                        changes_flag = True
                        break  # make the first advantageous exchange
                    else:
                        # swap back positions
                        # swap_positions(sorted_list, index2, index)
                        sorted_list[index2], sorted_list[index] = sorted_list[index], sorted_list[index2]

    return node_list, row_list, updated_net_list


def swap_positions(data_list: list, position1: int, position2: int):
    data_list[position1], data_list[position2] = data_list[position2], data_list[position1]
