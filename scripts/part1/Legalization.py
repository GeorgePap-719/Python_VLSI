# Tetris-like legalization algorithm
import operator

from scripts.classes.Node import Node
from scripts.classes.Row import Row
from scripts.part1.Overlaps import simple_do_overlap


# TODO Wip
def lr_legalizing_tetris_like_algo(node_list: list, row_list: list, net_list: list):
    legalized_node_list: list = []
    for row in row_list:
        legalized_row_nodes = []
        # starting to create new list of nodes because we are not sure in which state will be the data.
        # sort list based on x attribute
        sorted_list = sorted(row.row_nodes, key=operator.attrgetter('node_x'))
        negative_counter = -1
        for index, node in sorted_list:

            best_left_move = 0
            best_right_move = 0

            if (index % 2) == 1:
                node = node[negative_counter]
                negative_counter -= negative_counter
                # check if it is at the end of the line then we are ok e.g. right (x) = 100
                if node.node_x + node.node_width != row.lower_right_x_coordinate:
                    print("TODO")

                print("TODO")
            else:
                # check if it is at the start of the line then we are ok e.g. left (x) = 0
                if node.node_x != 0:
                    print("TODO")

                print("TODO")


def legalizing_tetris_like_algo(node_list: list, row_list: list, net_list: list):
    legalized_node_list: list = []
    for row in row_list:
        legalized_row_nodes = []
        # starting to create new list of nodes because we are not sure in which state will be the data.
        # sort list based on x attribute
        sorted_list = sorted(row.row_nodes, key=operator.attrgetter('node_x'))
        # check to find the most left node and continue to find the next
        for index, node in enumerate(sorted_list):
            # check if it is at the start of the line then we are ok e.g. left (x) = 0
            if node.node_x != 0:
                # calculate for each node every step that is possible
                best_move = 0
                for current_move in range(row.lower_right_x_coordinate):
                    # we are in the most right object or the row has only one object
                    if index + 1 == len(sorted_list):
                        # TODO check for the case where there is only one object
                        # if we had different input here we would get index out of bounds
                        if do_not_overlap_but_has_space_left(node, sorted_list[index - 1], current_move):
                            if best_move < current_move and \
                                    node.node_x - best_move >= 0:
                                best_move = current_move

                    else:
                        if index == 0:
                            if can_we_move_left(node, current_move):
                                if best_move < current_move and \
                                        node.node_x - best_move >= 0:
                                    best_move = current_move

                        else:
                            # if index + 1 != len(sorted_list):  # Not sure how the iteration gets in here
                            if do_not_overlap_but_has_space_left(node, sorted_list[index - 1], current_move):
                                if best_move < current_move and \
                                        node.node_x - best_move >= 0:
                                    best_move = current_move

                node.node_x = node.node_x - best_move

            legalized_node_list.append(node)
            legalized_row_nodes.append(node)
            # after we move the node, we take as guarantee that we are done with it.
            # continue each step for all nodes in the row

        row.row_nodes = legalized_row_nodes

    updated_net_list = update_net_list(net_list, legalized_node_list)
    updated_node_list = update_node_list(node_list, legalized_node_list)
    # row_list is already updated
    return updated_node_list, row_list, updated_net_list


def update_net_list(net_list: list, legalized_node_list: list) -> list:
    updated_net_list = []
    updated_net_nodes = []

    for net in net_list:
        for node in net.net_nodes:
            if node.node_type == "Terminal":
                updated_net_nodes.append(node)
            else:
                updated_net_nodes.append(get_node_name_in_list(node.node_name, legalized_node_list))

        net.net_nodes = updated_net_nodes
        net.find_coordinates_of_net()
        updated_net_list.append(net)

    return updated_net_list


def update_node_list(node_list: list, legalized_node_list: list):
    updated_node_list = []
    for node in node_list:
        if node.node_type == "Terminal":
            updated_node_list.append(node)
        else:
            updated_node_list.append(get_node_name_in_list(node.node_name, legalized_node_list))

    return updated_node_list


def get_node_name_in_list(node_name: str, node_list: list):
    for node in node_list:
        if node_name == node.node_name:
            return node


def do_not_overlap(node1: Node, node2: Node) -> bool:
    if simple_do_overlap(node1, node2):
        return False
    else:
        return True


def do_not_overlap_with_both_sides(left_node: Node, core_node: Node, right_node: Node) -> bool:
    if do_not_overlap(left_node, core_node) and do_not_overlap(core_node, right_node):
        return True
    else:
        return False


def do_overlap_but_has_space_left(core_node: Node, node_that_can_not_be_moved: Node, row: Row,
                                  current_move: int) -> bool:
    if simple_do_overlap(core_node, node_that_can_not_be_moved) and \
            can_we_move_left_without_overlapping(core_node, node_that_can_not_be_moved, current_move):
        return True
    else:
        return False


def can_we_move_left(left_node: Node, current_move) -> bool:
    if left_node.node_x - current_move >= 0:
        return True
    else:
        return False


def do_not_overlap_but_has_space_left(core_node: Node, unmovable_node: Node, current_move: int) -> bool:
    if do_not_overlap(unmovable_node, core_node) and \
            can_we_move_left_without_overlapping(core_node, unmovable_node, current_move):
        return True
    else:
        return False


def can_we_move_left_without_overlapping(current_node: Node, last_node: Node, current_move: int) -> bool:
    if current_node.node_x - current_move >= last_node.node_x + last_node.node_width:
        return True
    else:
        return False
