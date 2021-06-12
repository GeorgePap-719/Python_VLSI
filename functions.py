# parsing bookshelf-formatted designs

""""   Set the current working dir infos   """

import os

folderName = "ibm01_mpl6_placed_and_nettetris_legalized"
fileName = "ibm01"

os.chdir('C:\\Users\\root\\Desktop\\Designs_Viglas\\ISPD\\{}'.format(folderName))

""""    Classes    """


# (number of cells + number of i/o pins) (node = cell or i/o pin, terminal = i/o pin)
#     # NumTerminals : 8 (number of i/o pins)
#     # a1 14 10 (name, width, height)
class Node:

    def __init__(self, node_name, nodeWidth, nodeHeight, nodeType, nodeX=0, nodeY=0):
        self.nodeName = node_name
        self.nodeWidth = nodeWidth
        self.nodeHeight = nodeHeight
        self.nodeType = nodeType
        self.nodeX = nodeX
        self.nodeY = nodeY

    # update the Coordinates x & y
    def set_x_y(self, node_x, node_y):
        self.nodeX = node_x
        self.nodeY = node_y

    def __str__(self):
        return (str(self.nodeName) + " " + str(self.nodeWidth) + " " +
                str(self.nodeHeight) + " " + str(self.nodeType) + " " +
                str(self.nodeX) + " " + str(self.nodeY))


# TODO add comments
class Net:

    def __init__(self, net_name, net_degree):
        self.netName = net_name
        self.netDegree = net_degree
        self.netNodes = []  # list of nodes for the current net

    # appending the nodes that are part of this net
    def append_node(self, node):
        self.netNodes.append(node)

    # displaying Net infos and the nodes that are part of it
    def display_net(self):
        print("\n***")
        print(str(self.netName) + " - netDegree =  " + str(self.netDegree))
        print("Nodes of this net: ")
        for i in self.netNodes:
            print(i, end=" ")

    # not displaying the nodes that are part of the net
    def __str__(self):
        return str(self.netName) + " " + str(self.netDegree)

    """
    #testing the list of nodes -> h lista einai attribute tis klasis net
    def oeo(self):   
        print("\n" + str(self.netName) )
        print(type(self.netNodes), len(self.netNodes))
        for i in self.netNodes:
            print(i)
    """


class Row:

    def __init__(self, rowName, yMin, yMax, xMin, xMax):
        self.rowName = rowName
        self.yMin = yMin
        self.yMax = yMax
        self.xMin = xMin
        self.xMax = xMax

    def __str__(self):
        return (str(self.rowName) + " - yMin: " + str(self.yMin) + " -yMax: " +
                str(self.yMax) + " - xMin: " + str(self.xMin) + " - xMax: " +
                str(self.xMax))


""""    Functions   """


def verifyFiles():
    import time

    ext_tuple = [".aux", ".nets", ".nodes", ".pl", ".scl", ".wts"]
    flag = True

    list_ext = []

    name = 0
    extensions = 0
    for f in os.listdir():
        name, extensions = os.path.splitext(f)
        list_ext.append(extensions)

    # Sort them both, in order to compare them
    ext_tuple.sort()
    list_ext.sort()

    fixed_length = len(ext_tuple)
    readLen = len(list_ext)

    if ext_tuple == list_ext:

        if os.stat('{}.aux'.format(name)).st_size == 0:
            flag = False
            print(".aux file is empty")

        if (os.stat('{}.nodes'.format(name)).st_size == 0):
            flag = False
            print(".nodes file is empty")

        if (os.stat('{}.scl'.format(name)).st_size == 0):
            flag = False
            print(".scl file is empty")

        if (os.stat('{}.pl'.format(name)).st_size == 0):
            flag = False
            print(".pl file is empty")

        if (os.stat('{}.nets'.format(name)).st_size == 0):
            flag = False
            print(".scl file is empty")

        if (os.stat('{}.wts'.format(name)).st_size == 0):
            flag = False
            print(".wts file is empty")

        print("\n")

        # Exiting message
        if flag is False:
            time.sleep(1)
            print("Shutting down", end="")
            time.sleep(1)
            print(".", end="")
            time.sleep(1)
            print(".", end="")
            time.sleep(1)
            print(".", end="")
        else:
            print("\n- All files are verified!")

    elif fixed_length > readLen:
        flag = False
        print("- Some files are missing.\n")

        # exiting message
        time.sleep(1)
        print("Shutting down", end="")
        time.sleep(1)
        print(".", end="")
        time.sleep(1)
        print(".", end="")
        time.sleep(1)
        print(".", end="")

    else:
        flag = False
        print("- There are more files!\n")

        # exiting message
        time.sleep(1)
        print("Shutting down", end="")
        time.sleep(1)
        print(".", end="")
        time.sleep(1)
        print(".", end="")
        time.sleep(1)
        print(".", end="")

    return flag


def parser():
    """               Start of Parse .nodes               """

    file = open("{}.nodes".format(fileName))
    lines = file.readlines()

    saved = 0
    node_list = []  # List of all nodes for the current circuit

    # Locate NumNodes + NumTerminals
    for i in range(len(lines)):

        # TODO better name
        temp_parsing = lines[i].strip(" ,.\n#:").upper()  # upper everything cause of insensitive chars

        # Locate NumNodes
        if temp_parsing.find("NUMNODES") != -1:
            point = temp_parsing.find("NUMNODES")
            length = len("NUMNODES")

            num_nodes = temp_parsing[point + length:]
            num_nodes = num_nodes.strip(": ")

            # num_nodes = int(num_nodes) maybe for later use.

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

        node_name = temp[0]  # Node Name
        node_width = int(temp[1])  # Node Width  - Platos
        node_height = int(temp[2])  # Node Height  - Ypsos
        node_type = ""

        if len(temp) == 3:  # len == 3 -> Non Terminal
            node_type = "Non - Terminal"
        elif len(temp) == 4:  # len == 4 -> Terminal
            node_type = "Terminal"
        else:
            # Length is not 3 or 4 - Modified file
            print("Error. File is modified!")

        new_node = Node(node_name, node_width, node_height, node_type)
        node_list.append(new_node)  # nodeX,nodeY not found yet

    file.close()  # Close .nodes file

    """               End of Parse .nodes               """

    """
    for i in nodeList:
        print(i)
    """

    """               Start of Parse .pl               """

    file = open("{}.pl".format(fileName))  # open .pl file
    lines = file.readlines()

    # Skip first 4 lines
    for i in range(4, len(lines)):
        temp_parsing = lines[i].strip()
        temp_parsing = temp_parsing.split()

        node_name = temp_parsing[0]  # Node Name
        nodeX = int(temp_parsing[1])  # Lower Left Corner x

        # tempParsing[2] also includes " : N ...."
        # Need to filter it, in order to obtain 'y'
        temp_parsing[2] = temp_parsing[2].split(":")  # TODO check it

        node_y = int(temp_parsing[2][0])  # Lower Left Corner y

        # match the nodeNames and
        # update the nodeX,nodeY according to their coordinates
        for node in node_list:
            if node.nodeName == node_name:
                node.set_x_y(nodeX, node_y)

    file.close()  # Close .pl file
    """               End of Parse .pl               """

    """          
    for i in nodeList:
        print(i)
    """

    """               Start of Parse .nets               """

    file = open("{}.nets".format(fileName))  # open .nets file
    lines = file.readlines()

    saved = 0
    netList = []  # List of all nets for the current circuit

    # Locate NumNets
    for i in range(len(lines)):

        temp_parsing = lines[i].strip(" ,.\n#:").upper()

        # Parse NumNets
        if temp_parsing.find("NUMNETS") != -1:
            point = temp_parsing.find("NUMNETS")
            length = len("NUMNETS")

            numNets = temp_parsing[point + length:]
            numNets = numNets.strip(": ")

            numNets = int(numNets)

            saved = i
            break

    # Locating all NetDegree's
    # Filtering with .split
    name_nets_counter = -1
    for i in range(saved, len(lines)):

        # TODO add comment?
        temp_parsing = lines[i].strip(" ,.\n#:").upper()

        # Locate NetDegree
        if temp_parsing.find("NETDEGREE") != -1:

            name_nets_counter += 1

            temp_parsing = temp_parsing.replace(":", " ")
            temp_parsing = temp_parsing.split()

            # print(tempParsing,type(tempParsing))

            netDegree = int(temp_parsing[1])
            netName = "net{}".format(name_nets_counter)

            # print(netName)

            # Read the "netDegree" number of lines of each Net
            # netDegree+1 because "range" stops at (max - 1)
            # Starting from 1, to skip the " NetDegree : x " line
            newNet = Net(netName, netDegree)

            for j in range(1, netDegree + 1):
                nextLine = lines[i + j].split()  # contains node name & more
                currentNode = str(nextLine[0])  # parse only the node name

                newNet.append_node(currentNode)

            netList.append(newNet)  # append every net on the list of nets

    file.close()  # Close .nets file
    """               End of Parse .nets               """

    """                   
    a = 0 
    for i in netList:
        a = a+1
        #i.displayNet()
        i.oeo()
        if a == 20:
            break
    """

    """               Start of Parse .scl               """

    file = open("{}.scl".format(fileName))  # open .scl file
    lines = file.readlines()

    rowList = []  # List of all rows for the current circuit

    name_nets_counter = -1  # counter for name of the Rows
    for i in range(len(lines)):

        temp_parsing = lines[i].strip(" ,.\n#:").upper()

        if temp_parsing.find("COREROW HORIZONTAL") != -1:
            name_nets_counter += 1  # +1 for the next Row Name

            rowName = "row{}".format(name_nets_counter)  # Row Name

            # Parse Row's Coordinate and check if Coordinate is at (i+1) position
            # (i+1) = Coordinate
            temp = lines[i + 1].strip(" ,.\n#:").upper()

            if temp.find("COORDINATE") != -1:

                point = temp.find("COORDINATE")
                length = len("COORDINATE")

                rowCoord = temp[point + length:]

                rowCoord = rowCoord.strip(": ")
                # Lower Left Corner y coordinate of the row
                rowCoord = int(rowCoord)

            else:
                print("Error: File is modified.")

            # Parse Row's Height and check if Height is at (i+2) position
            # (i+2) = Height
            temp = lines[i + 2].strip(" ,.\n#:").upper()

            if temp.find("HEIGHT") != -1:

                point = temp.find("HEIGHT")
                length = len("HEIGHT")

                rowHeight = temp[point + length:]

                rowHeight = rowHeight.strip(": ")
                rowHeight = int(rowHeight)  # Row Height

            else:
                print("Error: File is modified.")

            # Parse SubRow Origin & Numsites & check if their position is (at i+7)
            # (i+7) = SubrowOrigin + Numsites
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
                    numSites = row_sub[point2 + length:]

                    numSites = numSites.strip(": ")
                    numSites = int(numSites)  # Lower Right Corner x Coordinate

                    # filter and locate SubrowOrigin
                    row_sub = row_sub[:point2]
                    row_sub = int(row_sub)  # Lower Left Corner x Coordinate

            else:
                print("Error: File is modified.")

            # rowHeight + rowCoord = yMax of each row
            new_row = Row(rowName, rowCoord,
                          (rowHeight + rowCoord), row_sub, numSites)

            rowList.append(new_row)  # append every row on the list of rows

    file.close()  # Close .scl file
    """               End of Parse .scl              """

    """
    for i in rowList:
        print(i)
    """
