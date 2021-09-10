import copy

from natsort import *

from scripts.classes.Net import total_calculate_net_wirelength
from scripts.classes.Node import Node
from scripts.part1.Legalization import legalizing_tetris_like_algo


# noinspection DuplicatedCode
def first_detailed_placement(node_list: list, row_list: list, net_list: list):
    # update_net(net_list)
    # print(total_calculate_net_wirelength(net_list))
    # total_calculate_net_wirelength is already 7680 before it gets in here.
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
                if index2 != index:
                    # All possible pairs, excluding duplicates
                    if node.node_width == node2.node_width:
                        swap_positions(sorted_list, index, index2)
                        update_net(updated_net_list)
                        new_wirelength = total_calculate_net_wirelength(updated_net_list)
                        if new_wirelength < wirelength:
                            print("found better wirelength")
                            wirelength = new_wirelength
                            changes_flag = True
                            break  # make the first advantageous exchange
                        else:
                            # swap back positions
                            swap_positions(sorted_list, index2, index)
                            update_net(updated_net_list)

    return node_list, row_list, updated_net_list


# noinspection DuplicatedCode
def second_detailed_placement(node_list: list, row_list: list, net_list: list):
    updated_net_list: list = copy.deepcopy(net_list)
    changes_flag = True
    wirelength = total_calculate_net_wirelength(net_list)

    # we stop only when there are no more changes that lead to better result
    while changes_flag:
        changes_flag = False
        for index, node in enumerate(node_list):
            if index + 1 == len(node_list):
                break
            for index2, node2 in enumerate(node_list):
                if index2 != index:
                    # All possible pairs, excluding duplicates
                    if node.node_width == node2.node_width:
                        swap_positions(node_list, index, index2)
                        update_net(updated_net_list)
                        new_wirelength = total_calculate_net_wirelength(updated_net_list)
                        if new_wirelength > wirelength:
                            print("found better wirelength")
                            wirelength = new_wirelength
                            changes_flag = True
                            # Notice how there is no break here, we make the most optimal change
                        else:
                            # swap back positions
                            swap_positions(node_list, index2, index)
                            update_net(updated_net_list)

    return node_list, row_list, updated_net_list


# noinspection DuplicatedCode
def third_detailed_placement(node_list: list, row_list: list, net_list: list):
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
                if index2 != index:
                    # All possible pairs, excluding duplicates
                    if node.node_width == node2.node_width:
                        swap_positions(sorted_list, index, index2)
                        update_net(updated_net_list)
                        new_wirelength = total_calculate_net_wirelength(updated_net_list)
                        if new_wirelength < wirelength:
                            print("found better wirelength")
                            wirelength = new_wirelength
                            changes_flag = True
                            break  # make the first advantageous exchange
                        else:
                            # swap back positions
                            swap_positions(sorted_list, index2, index)
                            update_net(updated_net_list)

        legalizing_tetris_like_algo(sorted_list, row_list, updated_net_list)

    return node_list, row_list, updated_net_list


# noinspection DuplicatedCode
def fourth_detailed_placement(node_list: list, row_list: list, net_list: list):
    updated_net_list: list = copy.deepcopy(net_list)
    changes_flag = True
    wirelength = total_calculate_net_wirelength(net_list)

    # we stop only when there are no more changes that lead to better result
    while changes_flag:
        changes_flag = False
        for index, node in enumerate(node_list):
            if index + 1 == len(node_list):
                break
            for index2, node2 in enumerate(node_list):
                if index2 != index:
                    # All possible pairs, excluding duplicates
                    if node.node_width == node2.node_width:
                        swap_positions(node_list, index, index2)
                        update_net(updated_net_list)
                        new_wirelength = total_calculate_net_wirelength(updated_net_list)
                        if new_wirelength < wirelength:
                            print("found better wirelength")
                            wirelength = new_wirelength
                            changes_flag = True
                            # Notice how there is no break here, we make the most optimal change
                        else:
                            # swap back positions
                            swap_positions(node_list, index2, index)
                            update_net(updated_net_list)

        legalizing_tetris_like_algo(node_list, row_list, updated_net_list)

    return node_list, row_list, updated_net_list


def swap_positions(data_list: list, position1: int, position2: int):
    node1: Node = data_list[position1]
    node2: Node = data_list[position2]
    temp_node: Node = data_list[position1]  # dumb data

    # swap
    # noinspection PyUnboundLocalVariable
    temp_node.node_x = node1.node_x
    # temp_node.node_width = node1.node_width
    temp_node.node_y = node1.node_y

    node1.node_x = node2.node_x
    # node1.node_width = node2.node_width
    node1.node_y = node2.node_y

    node2.node_x = temp_node.node_x
    # node2.node_width = temp_node.node_width
    node2.node_y = temp_node.node_y


def update_net(net_list: list):
    for net in net_list:
        net.find_coordinates_of_net()
        net.calculate_net_wirelength()
