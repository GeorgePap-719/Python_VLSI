from scripts import functions
from scripts.part1.Legalization import lr_legalizing_tetris_like_algo
from scripts.part1.Model import modeling
from scripts.part1.Overlaps import count_overlaps_in_row_list

if __name__ == "__main__":
    # if verify_files():
    #     parser()
    #
    # else:
    #     pass

    # change to appropriate path. If the path is not needed it can be left blank ("")
    path_to_designs = "../docs/designs/design/"

    print("parsing the files")
    node_list, row_list, net_list = functions.parser(path_to_designs)

    print("modeling the graph")
    modeling(node_list, row_list, net_list)

    print("counting overlaps")
    print(count_overlaps_in_row_list(row_list))

    print("Wire length")
    # print(total_calculate_net_wirelength(net_list))

    print("Legalizing with Tetris-like algorithm")
    # legalized_node_list, legalized_row_list, legalized_net_list = legalizing_tetris_like_algo(node_list, row_list,
    #                                                                                           net_list)

    # modeling(legalized_node_list, legalized_row_list, legalized_net_list)

    print("overlaps in legalized row_list")
    # print(count_overlaps_in_row_list(legalized_row_list))

    print("Wire length")
    # print(total_calculate_net_wirelength(legalized_net_list))

    print("Legalizing with second Tetris-like algorithm")
    legalized2_node_list, legalized2_row_list, legalized2_net_list = lr_legalizing_tetris_like_algo(node_list, row_list,
                                                                                                    net_list)

    modeling(legalized2_node_list, legalized2_row_list, legalized2_net_list)

    print("overlaps in second legalized row_list")
    print(count_overlaps_in_row_list(legalized2_row_list))
