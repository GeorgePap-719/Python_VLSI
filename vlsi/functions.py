# parsing bookshelf-formatted designs

""""   Set the current working dir infos   """

import os

from vlsi.classes.Net import Net
from vlsi.classes.Node import Node
from vlsi.classes.Row import Row
from vlsi.classes.Design import Design

"""
folderName = "ibm01_mpl6_placed_and_nettetris_legalized"
fileName = "ibm01"

os.chdir('C:\\Users\\root\\Desktop\\Python_Pandas\\docs\\ISPD\\{}'.format(
    folderName))
"""

folderName = "design"
fileName = "design"
# os.chdir('C:\\Users\\root\\Desktop\\Python_Pandas\\docs\\{}'.format(folderName)) uncomment when need it

""""    Functions   """


def exit_message():
    import time

    time.sleep(1)
    print("Shutting down", end="")
    time.sleep(1)
    print(".", end="")
    time.sleep(1)
    print(".", end="")
    time.sleep(1)
    print(".", end="")


def verify_files():
    flag = True

    extensions_tuple = [".aux", ".nets", ".nodes", ".pl", ".scl", ".wts"]

    extensions_list = []
    name = None

    for f in os.listdir():
        name, extensions = os.path.splitext(f)
        extensions_list.append(extensions)

    # Sort them both, in order to compare them
    extensions_tuple.sort()
    extensions_list.sort()

    fixed_length = len(extensions_tuple)
    read_length = len(extensions_list)

    if extensions_tuple == extensions_list:

        if os.stat('{}.aux'.format(name)).st_size == 0:
            flag = False
            print(".aux file is empty")

        if os.stat('{}.nodes'.format(name)).st_size == 0:
            flag = False
            print(".nodes file is empty")

        if os.stat('{}.scl'.format(name)).st_size == 0:
            flag = False
            print(".scl file is empty")

        if os.stat('{}.pl'.format(name)).st_size == 0:
            flag = False
            print(".pl file is empty")

        if os.stat('{}.nets'.format(name)).st_size == 0:
            flag = False
            print(".scl file is empty")

        if os.stat('{}.wts'.format(name)).st_size == 0:
            flag = False
            print(".wts file is empty")

        print("\n")

        if flag is False:
            exit_message()
        else:
            print("\n- All files are verified!")

    elif fixed_length > read_length:
        flag = False
        print("- Some files are missing.\n")
        exit_message()

    else:
        flag = False
        print("- There are more files!\n")
        exit_message()

    return flag


def parser(path):  # parsing the whole circuit

    """               Start of Parse .nodes               """

    file = open("{}{}.nodes".format(path, fileName))
    lines = file.readlines()

    saved = 0
    node_list = []  # List of all nodes for the current circuit
    number_of_nodes = None
    number_of_terminals = None
    number_of_nets = None

    # Locate NumNodes + NumTerminals
    for i in range(len(lines)):
        # .upper everything cause of insensitive chars
        temp_parsing = lines[i].strip(" ,.\n#:").upper()

        # Locate NumNodes
        if temp_parsing.find("NUMNODES") != -1:
            point = temp_parsing.find("NUMNODES")
            length = len("NUMNODES")

            number_of_nodes = temp_parsing[point + length:]
            number_of_nodes = number_of_nodes.strip(": ")

            number_of_nodes = int(number_of_nodes)

        # Locate NumTerminals
        if temp_parsing.find("NUMTERMINALS") != -1:
            point = temp_parsing.find("NUMTERMINALS")
            length = len("NUMTERMINALS")

            number_of_terminals = temp_parsing[point + length:]
            number_of_terminals = number_of_terminals.strip(": ")

            number_of_terminals = int(number_of_terminals)

            # Starting point for the 2nd for, +1 for the next line.
            saved = i + 1
            break

    # Parsing the Nodes
    for j in range(saved, len(lines)):

        temp = lines[j].strip("\t,.\n#: ")
        temp = temp.split()

        node_name = temp[0]
        node_width = int(temp[1])
        node_height = int(temp[2])

        if len(temp) == 3:  # len == 3 -> Non_Terminal
            node_type = "Non_Terminal"
        elif len(temp) == 4:  # len == 4 -> Terminal
            node_type = "Terminal"
        else:
            # Length is not 3 or 4 - Modified file
            print("Error. File is modified!")
            node_type = "Error. File is modified!"

        new_node = Node(node_name, node_width, node_height, node_type)
        node_list.append(new_node)  # node_x,node_y not found yet

    file.close()  # Close .nodes file

    """               End of Parse .nodes               """

    """               Start of Parse .pl               """

    file = open("{}.pl".format(fileName))
    lines = file.readlines()

    # Skip first 2 lines - comments
    for i in range(2, len(lines)):
        temp_parsing = lines[i].strip()
        temp_parsing = temp_parsing.split()  # temp_parsing type = list

        node_name = temp_parsing[0]    # todo it is used, check if below
        node_x = int(temp_parsing[1])  # Lower Left Corner x Coordinate
        node_y = int(temp_parsing[2])  # Lower Left Corner y Coordinate

        # match the node_names and
        # update the node_x,node_y according to their coordinates
        for node in node_list:
            if node.node_name == node_name:
                node.set_x_y(node_x, node_y)
                if node.node_type == "Non_Terminal":
                    node.set_points(node_x, node_x + node.node_width,
                                    node_y, node_y + node.node_height)

    file.close()  # Close .pl file
    """               End of Parse .pl               """

    """               Start of Parse .nets               """

    file = open("{}.nets".format(fileName))
    lines = file.readlines()

    saved = 0  # saving pointers that are used for parsing
    net_list = []  # List of all nets for the current circuit

    # Locate NumNets
    for i in range(len(lines)):

        temp_parsing = lines[i].strip(" ,.\n#:").upper()

        # Parse NumNets
        if temp_parsing.find("NUMNETS") != -1:
            point = temp_parsing.find("NUMNETS")
            length = len("NUMNETS")

            number_of_nets = temp_parsing[point + length:]
            number_of_nets = number_of_nets.strip(": ")

            number_of_nets = int(number_of_nets)

            saved = i
            break

    # Locating all NetDegree's
    name_counter = -1  # counter for names of the Nets
    for i in range(saved, len(lines)):

        temp_parsing = lines[i].strip(" ,.\n#:").upper()

        # Locate NetDegree
        if temp_parsing.find("NETDEGREE") != -1:

            name_counter += 1  # +1 for the next Net Name

            temp_parsing = temp_parsing.replace(":", " ")
            temp_parsing = temp_parsing.split()

            net_degree = int(temp_parsing[1])
            net_name = "net{}".format(name_counter)

            # Read the "netDegree" number of lines of each Net
            # netDegree+1 because "range" stops at (max - 1)
            # Starting from 1, to skip the " NetDegree : x " line

            new_net = Net(net_name, net_degree)

            for j in range(1, net_degree + 1):
                next_line = lines[i + j].split()  # contains node name & more
                current_node = str(next_line[0])  # parse only the node name

                # match the node name, to the node object
                for node in node_list:
                    if node.node_name == current_node:
                        new_net.append_node(node)

                # new_net.append_node(current_node)   #it appends node name

                # find on which nets, the current_node belongs to
                # and then updating the net_list of the current_node
                # according to the matches
                for node in node_list:
                    if node.node_name == current_node:
                        node.append_net(new_net.net_name)

            new_net.find_coordinates_of_net()
            new_net.calculate_net_wirelength()
            new_net.calculate_net_size()
            net_list.append(new_net)  # add every net on the list of nets

    file.close()  # Close .nets file
    """               End of Parse .nets               """

    """               Start of Parse .scl               """

    file = open("{}.scl".format(fileName))
    lines = file.readlines()

    row_name = None         #todo it is also used, check below
    row_coordinate = None
    row_sub = None
    row_numsites = None
    row_height = None

    row_list = []  # List of all rows for the current circuit

    name_counter = -1  # counter for name of the Rows
    for i in range(len(lines)):
        # .upper everything cause of insensitive chars
        temp_parsing = lines[i].strip(" ,.\n#:").upper()

        if temp_parsing.find("COREROW HORIZONTAL") != -1:
            name_counter += 1  # +1 for the next Row Name

            row_name = "row{}".format(name_counter)

            # Parse Row's Coordinate and check if Coordinate is at (i+1)
            # position
            # (i+1) = Coordinate
            # .upper everything cause of insensitive chars
            temp = lines[i + 1].strip(" ,.\n#:").upper()

            if temp.find("COORDINATE") != -1:

                point = temp.find("COORDINATE")
                length = len("COORDINATE")

                row_coordinate = temp[point + length:]
                row_coordinate = row_coordinate.strip(": ")

                # Lower Left Corner y coordinate of the row
                row_coordinate = int(row_coordinate)

            else:
                print("Error: File is modified.")

            # Parse Row's Height and check if Height is at (i+2) position
            # (i+2) = Height
            # .upper everything cause of insensitive chars
            temp = lines[i + 2].strip(" ,.\n#:").upper()

            if temp.find("HEIGHT") != -1:

                point = temp.find("HEIGHT")
                length = len("HEIGHT")

                row_height = temp[point + length:]
                row_height = row_height.strip(": ")
                row_height = int(row_height)

            else:
                print("Error: File is modified.")

            # Parse SubrowOrigin & Numsites & check if their position is
            # at (i+7)
            # (i+7) = SubrowOrigin + Numsites
            # .upper everything cause of insensitive chars
            temp = lines[i + 7].strip(" ,.\n#:").upper()

            if temp.find("SUBROWORIGIN") != -1:

                point = temp.find("SUBROWORIGIN")
                length = len("SUBROWORIGIN")

                row_sub = temp[point + length:]
                row_sub = row_sub.strip(": ")
                row_sub = row_sub.strip(" ,.\n#:").upper()

                if row_sub.find("NUMSITES") != -1:
                    point2 = row_sub.find("NUMSITES")

                    # filter and locate Numsites
                    row_numsites = row_sub[point2 + length:]
                    row_numsites = row_numsites.strip(": ")

                    # Lower Right Corner x Coordinate
                    row_numsites = int(row_numsites)

                    # filter and locate SubrowOrigin
                    row_sub = row_sub[:point2]
                    row_sub = int(row_sub)  # Lower Left Corner x Coordinate

            else:
                print("Error: File is modified.")

            # row_height + row_coordinate = y_max of each row
            new_row = Row(row_name, row_coordinate,
                          (row_height + row_coordinate), row_sub, row_numsites)

            row_list.append(new_row)  # add every row on the list of rows

    file.close()  # Close .scl file
    """               End of Parse .scl              """
    # Find the row, each node is placed in
    for row in row_list:
        for node in node_list:
            # check for both lower_y and upper_y to avoid Terminal nodes
            if (node.lower_left_corner.y == row.lower_left_corner.y and
                    node.upper_left_corner.y == row.upper_left_corner.y):
                node.set_row(row)
                row.append_node(node)

    # Find the row(s), each Net belongs to and the opposite
    for net in net_list:
        for node in net.net_nodes:
            if node.node_type == "Non_Terminal":
                net.append_row(node.node_row)
                node.node_row.append_net(net)
        net.net_rows = list(dict.fromkeys(net.net_rows))  # remove duplicates

    # Update each row, with its density
    for row in row_list:
        row.calculate_row_density()

    # Design calculations
    design_infos = Design(number_of_nodes, number_of_terminals, number_of_nets)

    # TESTING PRINTS:

    """
    for net in net_list:
        net.display_net_rows()
        net.display_net_external_nodes()
        net.display_net_internal_nodes()
    print("\n\n**")
    """
    """
    for row in row_list:
        print("\n\n**")
        row.display_row_nets()
        row.display_row_nodes()
    """

    """
    for net in net_list:
        for row in net.net_rows:
            print(type(row.net_rows))
    """

    """
    for net in net_list:
        for node in node_list:
            if node.node_name == net.net
    """

    """
    for node in node_list:
        node.display_node_row()
    """

    """
    for row in row_list:
        row.display_row()
    """

    """
    for i in row_list:
        print(i)
    """

    """
    a = 0
    for i in node_list:
        a = a + 1
        i.display_node_corners()

        if a == 20:
            break

    """

    """
    a = 0
    for i in net_list:
        a += 1
        i.display_net()
        i.find_coordinates_of_net()
        i.calculate_net_wirelength()
        i.calculate_net_size()

        print("\n")

        i.display_net_size()
        i.display_net_wirelength()
        if a == 15:
            break
    """
