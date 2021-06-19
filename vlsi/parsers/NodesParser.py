# This class is designed to handle .nets files

# TODO delete it
# TODO add constructor to avoid compatibility issues on windows or linux due to different absolute paths.
class NodesParser:
    nodes_file = open("../../docs/designs/design/design.nodes", "r")
    print(nodes_file.read())

    # (number of cells + number of i/o pins) (node = cell or i/o pin, terminal = i/o pin)
    # NumTerminals : 8 (number of i/o pins)
    # a1 14 10 (name, width, height)
    @staticmethod
    def get_num_nodes(nodes_file):
        nodes_file.readlines()
        # print("TODO")

    @staticmethod
    def get_num_terminals(nodes_file):
        print("TODO")

    # def get_nodes(nodes_file) return (name, width, height)
    # TODO
