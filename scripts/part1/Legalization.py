import operator

from scripts.classes.Node import Node
from scripts.part1.Overlaps import simple_do_overlap


# noinspection DuplicatedCode
def lr_legalizing_tetris_like_algo(node_list: list, row_list: list, net_list: list):
    legalized_node_list: list = []
    for row in row_list:
        legalized_row_nodes = []
        negative_counter = -1  # -1 is the last object in a list, TODO better name
        counter = 0
        true_index = 0  # TODO better name

        # starting to create new list of nodes because we are not sure in which state will be the data.
        # sort list based on x attribute
        sorted_list: list[Node] = sorted(row.row_nodes, key=operator.attrgetter('node_x'))
        while counter + 1 <= len(sorted_list):
            upper_flag = False
            lower_flag = False

            best_left_move = 0
            best_right_move = 0
            # separate left and right instances
            if (counter % 2) == 1:
                new_index = negative_counter
                node = sorted_list[negative_counter]
                # check if it is at the end of the line then we are ok e.g. right (x) = 100
                if node.node_x + node.node_width != row.lower_right_x_coordinate:
                    for current_move in range(row.lower_right_x_coordinate):
                        # we are in the last object
                        if negative_counter == -1:
                            # TODO check for the case where there is only one object
                            # if we had different input here we would get index out of bounds
                            if do_not_overlap_but_has_space_left(node, sorted_list[new_index - 1], current_move):
                                if best_left_move < current_move and \
                                        node.node_x - best_left_move >= 0:
                                    best_left_move = current_move
                                    upper_flag = True

                            if can_we_move_right_without_overlapping(node, sorted_list[new_index - 1], current_move):
                                if best_right_move < current_move and \
                                        node.node_x + node.node_width + best_right_move <= 100:
                                    best_right_move = current_move
                                    lower_flag = True

                        else:
                            if can_we_move_left_without_overlapping_both_sides(node, sorted_list[new_index - 1],
                                                                               sorted_list[new_index + 1],
                                                                               current_move):
                                if best_left_move < current_move and \
                                        node.node_x - best_left_move >= 0:
                                    best_left_move = current_move
                                    upper_flag = True

                            if can_we_move_right_without_overlapping_both_sides(node, sorted_list[new_index - 1],
                                                                                sorted_list[new_index + 1],
                                                                                current_move):
                                if best_right_move < current_move and \
                                        node.node_x + node.node_width + best_right_move <= 100:
                                    best_right_move = current_move
                                    lower_flag = True

                    """ Since we decide which is the best move based on the shortest length between left and right moves
                    there is a case where if one block is already overlapped with another, the best move in its
                    corresponding direction results in 0 and it is picked as the best move for the node. The problem
                    is solved with simple True/False flag logic.
                    
                    :param upper_flag: is for best_left_moves
                    :param lower_flag: is for best_right_moves
                    """
                    if lower_flag is True and upper_flag is False:
                        node.node_x += best_right_move
                    elif upper_flag is True and lower_flag is False:
                        node.node_x -= best_left_move
                    else:
                        if best_right_move < best_left_move:
                            node.node_x += best_right_move
                        else:
                            node.node_x -= best_left_move

                    negative_counter += negative_counter

            else:
                node = sorted_list[true_index]
                # check if it is at the start of the line then we are ok e.g. left (x) = 0
                if node.node_x != 0:
                    for current_move in range(row.lower_right_x_coordinate):

                        # if list has only one object.
                        if true_index == 0 and true_index + 1 == len(sorted_list):
                            if can_we_move_left(node, current_move):
                                if best_left_move < current_move and \
                                        node.node_x - best_left_move >= 0:
                                    best_left_move = current_move
                                    upper_flag = True
                            if can_we_move_right(node, current_move):
                                if best_right_move < current_move and \
                                        node.node_x + node.node_width + best_right_move <= 100:
                                    best_right_move = current_move
                                    lower_flag = True

                        # we are in the first object
                        elif true_index == 0:
                            if can_we_move_left(node, current_move):
                                if best_left_move < current_move and \
                                        node.node_x - best_left_move >= 0:
                                    best_left_move = current_move
                                    upper_flag = True
                            if can_we_move_right_without_overlapping_with_next_node(node, sorted_list[true_index + 1],
                                                                                    current_move):
                                if best_right_move < current_move and \
                                        node.node_x + node.node_width + best_right_move <= 100:
                                    best_right_move = current_move
                                    lower_flag = True

                        # last object in the list
                        elif true_index + 1 == len(sorted_list):  # not getting in here anymore
                            if can_we_move_left_without_overlapping_both_sides(node, sorted_list[true_index - 1],
                                                                               sorted_list[true_index + 1],
                                                                               current_move):
                                if best_left_move < current_move and \
                                        node.node_x - best_left_move >= 0:
                                    best_left_move = current_move
                                    upper_flag = True
                            if can_we_move_right_without_overlapping_both_sides(node, sorted_list[true_index - 1],
                                                                                sorted_list[true_index + 1],
                                                                                current_move):
                                if best_right_move < current_move and \
                                        node.node_x + node.node_width + best_right_move <= 100:
                                    best_right_move = current_move
                                    lower_flag = True

                        # default case
                        else:
                            if can_we_move_left_without_overlapping_both_sides(node, sorted_list[true_index - 1],
                                                                               sorted_list[true_index + 1],
                                                                               current_move):
                                if best_left_move < current_move and \
                                        node.node_x - best_left_move >= 0:
                                    best_left_move = current_move
                                    upper_flag = True
                            if can_we_move_right_without_overlapping_both_sides(node, sorted_list[true_index - 1],
                                                                                sorted_list[true_index + 1],
                                                                                current_move):
                                if best_right_move < current_move and \
                                        node.node_x + node.node_width + best_right_move <= 100:
                                    best_right_move = current_move
                                    lower_flag = True

                    if lower_flag is True and upper_flag is False:
                        node.node_x += best_right_move
                    elif upper_flag is True and lower_flag is False:
                        node.node_x -= best_left_move
                    else:
                        if best_right_move < best_left_move:
                            node.node_x += best_right_move
                        else:
                            node.node_x -= best_left_move

                true_index += 1

            counter += 1
            legalized_node_list.append(node)
            legalized_row_nodes.append(node)

            # after we move the node, we take as guarantee that we are done with it.
            # continue each step for all nodes in the row
        row.row_nodes = legalized_row_nodes

    updated_net_list = update_net_list(net_list, legalized_node_list)
    updated_node_list = update_node_list(node_list, legalized_node_list)
    # row_list is already updated
    return updated_node_list, row_list, updated_net_list


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
        net.calculate_net_wirelength()
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


def can_we_move_left(left_node: Node, current_move) -> bool:
    if left_node.node_x - current_move >= 0:
        return True
    else:
        return False


def can_we_move_right(node: Node, current_move: int) -> bool:
    if node.node_x + node.node_width + current_move <= 100:  # max limit of row
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


def do_overlap_but_has_space_left(core_node: Node, unmovable_node: Node, current_move: int) -> bool:
    if simple_do_overlap(unmovable_node, core_node) and \
            can_we_move_left_without_overlapping(core_node, unmovable_node, current_move):
        return True
    else:
        return False


def can_we_move_right_without_overlapping(current_node: Node, last_node: Node, current_move: int) -> bool:
    if current_node.node_x + current_move >= last_node.node_x + last_node.node_width:
        return True
    else:
        return False


def can_we_move_right_without_overlapping_both_sides(current_node: Node, last_node: Node, next_node: Node,
                                                     current_move: int) -> bool:
    if last_node.node_x <= current_node.node_x + current_move \
            and current_node.node_x + current_node.node_width < next_node.node_x:
        # and current_node.node_x + current_move + current_node.node_width <= 100:
        return True
    else:
        return False


def can_we_move_left_without_overlapping_both_sides(current_node: Node, last_node: Node, next_node: Node,
                                                    current_move: int) -> bool:
    if last_node.node_x + last_node.node_width <= current_node.node_x - current_move and \
            current_node.node_x - current_move + current_node.node_width <= next_node.node_x:
        return True
    else:
        return False


def can_we_move_right_without_overlapping_with_next_node(current_node: Node, next_node: Node,
                                                         current_move: int) -> bool:
    if current_node.node_x + current_move <= next_node.node_x:
        return True
    else:
        return False
