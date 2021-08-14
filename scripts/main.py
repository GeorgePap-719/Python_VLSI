from scripts import functions
from scripts.part1.Model import modeling, count_overlaps_in_row_list

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
