# Tetris-like legalization algorithm
import operator

from scripts.classes.Node import Node
from scripts.classes.Row import Row
from scripts.part1.Model import do_overlap


def legalizing_tetris_like_algo(node_list: list, row_list: list, net_list: list):
    print("WIP")
    legalized_node_list: list
    for row in row_list:
        # starting to create new list of nodes because we are not sure in which state will be the data.
        # check to find the most left node and continue to find the next
        # sort list based on x attribute
        sorted_list = sorted(row.row_nodes, key=operator.attrgetter('node_x'))
        for index, node in enumerate(sorted_list):
            # check if it is at the start of the line then we are ok e.g. left (x) = 0
            if node.node_x == 0:
                continue
            # calculate for each node every step that is possible
            best_move = 0
            for current_move in range(row.lower_right_x_coordinate):
                # we are in the most right object
                if index + 1 > len(sorted_list):
                    if do_not_overlap_but_has_space_left(sorted_list[index], sorted_list[index - 1]):
                        if can_we_step_left(node.node_x, current_move, sorted_list[index - 1]):
                            best_move = current_move
                    elif do_overlap_but_has_space_right(sorted_list[index], sorted_list[index - 1]):
                        best_move = step_right_until_we_do_not_overlap(node.node_x, current_move,
                                                                       sorted_list[index - 1],
                                                                       row)
                else:
                    if node.node_x - current_move >= 0 and do_not_overlap(sorted_list[index], sorted_list[index + 1]):
                        best_move = current_move
            node.node_x = best_move
            legalized_node_list.append(node)
            # after we move the node, we take as guarantee that we are done with it.
            # continue each step for all nodes in the row
        row.row_nodes = legalized_node_list

    # TODO shouldn't we also change the nets?
    return legalized_node_list, row_list


def do_not_overlap(node1: Node, node2: Node) -> bool:
    return not do_overlap(node1, node2) == 1


def do_overlap_but_has_space_right(core_node: Node, node_that_can_not_be_moved: Node, row: Row) -> bool:
    if do_overlap(core_node, node_that_can_not_be_moved) and \
            can_we_move_right(core_node.node_x, row.lower_right_x_coordinate):
        return True
    else:
        return False


def do_not_overlap_but_has_space_left(right_node: Node, left_node: Node) -> bool:
    if do_not_overlap(left_node, right_node) and \
            can_we_move_left(right_node.node_x, left_node):
        return True
    else:
        return False


def can_we_step_left(node_x: int, current_move: int, last_node: Node) -> bool:
    if node_x - current_move >= last_node.node_x:
        return True
    else:
        return False


def can_we_move_left(node_x: int, last_node: Node) -> bool:
    if node_x - last_node.node_x >= 0:
        return True
    else:
        return False


def can_we_move_right(node_x: int, row_length: int) -> bool:
    if node_x - row_length >= 0:
        return True
    else:
        return False


def step_right_until_we_do_not_overlap(node_x: int, current_move: int, last_node: Node, row: Row) -> int:
    step = node_x + current_move
    if last_node.node_x <= step <= row.lower_right_x_coordinate:
        return step
    return 0  # in this scenario there is no move to make
