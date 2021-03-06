import copy

from scripts import functions
from scripts.classes.Net import total_calculate_net_wirelength
from scripts.part1.Legalization import legalizing_tetris_like_algo, lr_legalizing_tetris_like_algo
from scripts.part1.Model import modeling
from scripts.part1.Overlaps import count_overlaps_in_row_list
from scripts.part2.DataFrames import *
from scripts.part2.DetailPlacement import first_detailed_placement, second_detailed_placement

if __name__ == "__main__":
    # change to appropriate path. If the path is not needed it can be left blank ("")
    path_to_designs = "../docs/designs/design/"

    print("parsing the files")
    node_list, row_list, net_list = functions.parser(path_to_designs)

    lr_node_list = copy.deepcopy(node_list)
    lr_row_list = copy.deepcopy(row_list)
    lr_net_list = copy.deepcopy(net_list)

    print("modeling the graph")
    modeling(node_list, row_list, net_list)

    print("counting overlaps")
    print(count_overlaps_in_row_list(row_list))

    print("First Wire length")
    print(total_calculate_net_wirelength(net_list))

    print("Legalizing with Tetris-like algorithm")
    legalized_node_list, legalized_row_list, legalized_net_list = legalizing_tetris_like_algo(node_list, row_list,
                                                                                              net_list)

    modeling(legalized_node_list, legalized_row_list, legalized_net_list)

    print("overlaps in legalized row_list")
    print(count_overlaps_in_row_list(legalized_row_list))

    print("Wire length")
    print(total_calculate_net_wirelength(legalized_net_list))

    print("Legalizing with second Tetris-like algorithm")
    legalized2_node_list, legalized2_row_list, legalized2_net_list = lr_legalizing_tetris_like_algo(lr_node_list,
                                                                                                    lr_row_list,
                                                                                                    lr_net_list)

    print("Second Wire length")
    print(total_calculate_net_wirelength(legalized2_net_list))

    modeling(legalized2_node_list, legalized2_row_list, legalized2_net_list)

    print("overlaps in second legalized row_list")
    print(count_overlaps_in_row_list(legalized2_row_list))

    print("Third Wire length")
    print(total_calculate_net_wirelength(legalized_net_list))

    print("first detailed placement")
    detailed_placed_node_list, detailed_placed_row_list, detailed_placed_net_list = first_detailed_placement(
        legalized_node_list, legalized_row_list, legalized_net_list)

    print("after first detailed Wire length")
    print(total_calculate_net_wirelength(detailed_placed_net_list))

    print("second detailed placement")
    detailed2_placed_node_list, detailed2_placed_row_list, detailed2_placed_net_list = second_detailed_placement(
        legalized_node_list, legalized_row_list, legalized_net_list)

    print("after second detailed Wire length")
    print(total_calculate_net_wirelength(detailed2_placed_net_list))

    # Uncomment it
    # print("Third detailed placement")
    # detailed3_placed_node_list, detailed3_placed_row_list, detailed3_placed_net_list = third_detailed_placement(
    #     legalized_node_list, legalized_row_list, legalized_net_list)
    #
    # print("after third detailed Wire length")
    # print(total_calculate_net_wirelength(detailed3_placed_net_list))

    # print("Fourth detailed placement")
    # detailed4_placed_node_list, detailed4_placed_row_list, detailed4_placed_net_list = fourth_detailed_placement(
    #     legalized_node_list, legalized_row_list, legalized_net_list)
    #
    # print("after fourth detailed Wire length")
    # print(total_calculate_net_wirelength(detailed4_placed_net_list))

    # DataFrames

    # Nodes DataFrame Functions
    nodes_df = create_nodes_df(lr_node_list)
    print("\nDisplay Nodes Dataframe: \n")
    print(nodes_df)
    print("\n")

    # Nets DataFrame Functions
    # Erwthma 17: ypologismos emvadou enos net kaleitai mesa sto DataFrame
    nets_df = create_nets_df(lr_net_list, nodes_df)
    print("\nDisplay Nets Dataframe: \n")
    print(nets_df)
    print("\n")

    # Rows DataFrame Functions
    rows_df = create_rows_df(lr_row_list, nodes_df)
    print("\nDisplay Rows Dataframe: \n")
    print(rows_df)
    print("\n")

    # Design DataFrame Functions
    # Erwthma 16: To sinoliko mikos kalwdiou kaleitai mesa sto design_df
    design_df = create_design_df(nodes_df, nets_df, rows_df)
    print("\nDisplay Designs Dataframe: \n")
    print(design_df)
    print("\n")

    # Nodes Functions
    biggest_non_terminal_node(nodes_df)
    smallest_non_terminal_node(nodes_df)
    mean_size_non_terminal_nodes(nodes_df)
    print('\n')

    # Nets Functions
    biggest_net_based_on_nodes(nets_df)
    smallest_net_based_on_nodes(nets_df)
    print('\n')

    # Rows Functions
    smallest_row_based_on_density(rows_df)
    biggest_row_based_on_density(rows_df)
    mean_row_density(rows_df)
    print('\n')

    node_with_most_connections(nodes_df, nets_df)
    node_with_least_connections(nodes_df, nets_df)
    mean_number_of_node_connections(nodes_df, nets_df)

    swap_cells(nodes_df, nets_df, rows_df, design_df)
    insert_a_cell(nodes_df, nets_df, rows_df, design_df)