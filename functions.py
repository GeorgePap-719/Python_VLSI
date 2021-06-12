# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 18:27:44 2021

@author: root
"""


# 3rd try - parsing whole bookshelf in 1 file - creating functions & classes

""""   Set the current working dir infos   """

import os
folderName = "ibm01_mpl6_placed_and_nettetris_legalized"
fileName = "ibm01"

os.chdir('C:\\Users\\root\\Desktop\\Designs_Viglas\\ISPD\\{}'.format(folderName))


""""    Classes    """


class Node:

    def __init__(self, nodeName, nodeWidth, nodeHeight, nodeType, nodeX=0, nodeY=0):
        self.nodeName = nodeName
        self.nodeWidth = nodeWidth
        self.nodeHeight = nodeHeight
        self.nodeType = nodeType
        self.nodeX = nodeX
        self.nodeY = nodeY

    # update the Coordinates x & y
    def set_X_Y(self, nodeX, nodeY):
        self.nodeX = nodeX
        self.nodeY = nodeY

    def __str__(self):
        return (str(self.nodeName) + " " + str(self.nodeWidth) + " " +
                str(self.nodeHeight) + " " + str(self.nodeType) + " " +
                str(self.nodeX) + " " + str(self.nodeY))


class Net:

    def __init__(self, netName, netDegree):
        self.netName = netName
        self.netDegree = netDegree
        self.netNodes = []  # list of nodes for the current net

    # appending the nodes that are part of this net
    def appendNode(self, node):
        self.netNodes.append(node)

    # displaying Net infos and the nodes that are part of it
    def displayNet(self):
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

    for f in os.listdir():

        name, exte = os.path.splitext(f)
        list_ext.append(exte)

    # Sort them both, in order to compare them
    ext_tuple.sort()
    list_ext.sort()

    fixedLen = len(ext_tuple)
    readLen = len(list_ext)

    if ext_tuple == list_ext:

        if(os.stat('{}.aux'.format(name)).st_size == 0):
            flag = False
            print(".aux file is empty")

        if(os.stat('{}.nodes'.format(name)).st_size == 0):
            flag = False
            print(".nodes file is empty")

        if(os.stat('{}.scl'.format(name)).st_size == 0):
            flag = False
            print(".scl file is empty")

        if(os.stat('{}.pl'.format(name)).st_size == 0):
            flag = False
            print(".pl file is empty")

        if(os.stat('{}.nets'.format(name)).st_size == 0):
            flag = False
            print(".scl file is empty")

        if(os.stat('{}.wts'.format(name)).st_size == 0):
            flag = False
            print(".wts file is empty")

        print("\n")

        # Exiting message
        if(flag is False):
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

    elif fixedLen > readLen:
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

    f = open("{}.nodes".format(fileName))  # open .nodes file
    lines = f.readlines()

    saved = 0
    nodeList = []  # List of all nodes for the current circuit

    # Locate NumNodes + NumTerminals
    for i in range(len(lines)):

        tempParsing = lines[i].strip(" ,.\n#:").upper()

        # Locate NumNodes
        if tempParsing.find("NUMNODES") != -1:

            point = tempParsing.find("NUMNODES")
            leng = len("NUMNODES")

            numNodes = tempParsing[point+leng:]
            numNodes = numNodes.strip(": ")

            numNodes = int(numNodes)

        # Locate NumTerminals
        if tempParsing.find("NUMTERMINALS") != -1:

            point = tempParsing.find("NUMTERMINALS")
            leng = len("NUMTERMINALS")

            numTer = tempParsing[point+leng:]
            numTer = numTer.strip(": ")

            numTer = int(numTer)

            # Starting point for the 2nd for, +1 for the next line.
            saved = i + 1
            break

    # Parsing the Nodes
    for j in range(saved, len(lines)):

        temp = lines[j].strip("\t,.\n#: ")
        temp = temp.split()

        nodeName = temp[0]  # Node Name
        nodeWidth = int(temp[1])  # Node Width  - Platos
        nodeHeight = int(temp[2])  # Node Height  - Ypsos

        if len(temp) == 3:  # len == 3 -> Non Terminal
            nodeType = "Non - Terminal"
        elif len(temp) == 4:  # len == 4 -> Terminal
            nodeType = "Terminal"
        else:
            # Length isnt 3 or 4 - Modified file
            print("Error. File is modified!")

        newNode = Node(nodeName, nodeWidth, nodeHeight, nodeType)
        nodeList.append(newNode)  # nodeX,nodeY not found yet

    f.close()  # Close .nodes file

    """               End of Parse .nodes               """

    """
    for i in nodeList:
        print(i)
    """

    """               Start of Parse .pl               """

    f = open("{}.pl".format(fileName))  # open .pl file
    lines = f.readlines()

    # Skip first 4 lines
    for i in range(4, len(lines)):
        tempParsing = lines[i].strip()
        tempParsing = tempParsing.split()

        nodeName = tempParsing[0]  # Node Name
        nodeX = int(tempParsing[1])  # Lower Left Corner x

        # tempParsing[2] also includes " : N ...."
        # Need to filter it, in order to obtain 'y'
        tempParsing[2] = tempParsing[2].split(":")

        nodeY = int(tempParsing[2][0])  # Lower Left Corner y

        # match the nodeNames and
        # update the nodeX,nodeY accordind to their coordinates
        for node in nodeList:
            if (node.nodeName == nodeName):
                node.set_X_Y(nodeX, nodeY)

    f.close()  # Close .pl file
    """               End of Parse .pl               """

    """          
    for i in nodeList:
        print(i)
    """

    """               Start of Parse .nets               """

    f = open("{}.nets".format(fileName))  # open .nets file
    lines = f.readlines()

    saved = 0
    netList = []  # List of all nets for the current circuit

    # Locate NumNets
    for i in range(len(lines)):

        tempParsing = lines[i].strip(" ,.\n#:").upper()

        # Parse NumNets
        if tempParsing.find("NUMNETS") != -1:

            point = tempParsing.find("NUMNETS")
            leng = len("NUMNETS")

            numNets = tempParsing[point+leng:]
            numNets = numNets.strip(": ")

            numNets = int(numNets)

            saved = i
            break

    # Locating all NetDegree's
    # Filtering with .split
    nameCounter = -1  # counter for name of the Nets
    for i in range(saved, len(lines)):

        tempParsing = lines[i].strip(" ,.\n#:").upper()

        # Locate NetDegree
        if tempParsing.find("NETDEGREE") != -1:

            nameCounter += 1               # +1 for the next Net Name

            tempParsing = tempParsing.replace(":", " ")
            tempParsing = tempParsing.split()

            # print(tempParsing,type(tempParsing))

            netDegree = int(tempParsing[1])  # NetDegree
            netName = "net{}".format(nameCounter)  # Net Name

            # print(netName)

            # Read the "netDegree" number of lines of each Net
            # netDegree+1 because "range" stops at (max - 1)
            # Starting from 1, to skip the " NetDegree : x " line

            newNet = Net(netName, netDegree)

            for j in range(1, netDegree+1):
                nextLine = lines[i+j].split()  # contains node name & more
                currentNode = str(nextLine[0])  # parse only the node name

                newNet.appendNode(currentNode)

            netList.append(newNet)  # append every net on the list of nets

    f.close()  # Close .nets file
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

    f = open("{}.scl".format(fileName))  # open .scl file
    lines = f.readlines()

    rowList = []  # List of all rows for the current circuit

    nameCounter = -1  # counter for name of the Rows
    for i in range(len(lines)):

        tempParsing = lines[i].strip(" ,.\n#:").upper()

        if tempParsing.find("COREROW HORIZONTAL") != -1:
            nameCounter += 1        # +1 for the next Row Name

            rowName = "row{}".format(nameCounter)  # Row Name

            # Parse Row's Coordinate and check if Coordinate is at (i+1) position
            # (i+1) = Coordinate
            temp = lines[i+1].strip(" ,.\n#:").upper()

            if temp.find("COORDINATE") != -1:

                point = temp.find("COORDINATE")
                leng = len("COORDINATE")

                rowCoord = temp[point+leng:]
                rowCoord = rowCoord.strip(": ")
                # Lower Left Corner y coordinate of the row
                rowCoord = int(rowCoord)

            else:
                print("Error: File is modified.")

            # Parse Row's Height and check if Height is at (i+2) position
            # (i+2) = Height
            temp = lines[i+2].strip(" ,.\n#:").upper()

            if temp.find("HEIGHT") != -1:

                point = temp.find("HEIGHT")
                leng = len("HEIGHT")

                rowHeight = temp[point+leng:]
                rowHeight = rowHeight.strip(": ")
                rowHeight = int(rowHeight)  # Row Height

            else:
                print("Error: File is modified.")

            # Parse SubrowOrigin & Numsites & check if their position is (at i+7)
            # (i+7) = SubrowOrigin + Numsites
            temp = lines[i+7].strip(" ,.\n#:").upper()

            if temp.find("SUBROWORIGIN") != -1:

                point = temp.find("SUBROWORIGIN")
                leng = len("SUBROWORIGIN")

                rowSub = temp[point+leng:]
                rowSub = rowSub.strip(": ")
                rowSub = rowSub.strip(" ,.\n#:").upper()

                if rowSub.find("NUMSITES") != -1:
                    point2 = rowSub.find("NUMSITES")

                    # filter and locate Numsites
                    numSites = rowSub[point2+leng:]
                    numSites = numSites.strip(": ")
                    numSites = int(numSites)  # Lower Right Corner x Coordinate

                    # filter and locate SubrowOrigin
                    rowSub = rowSub[:point2]
                    rowSub = int(rowSub)  # Lower Left Corner x Coordinate

            else:
                print("Error: File is modified.")

            # rowHeight + rowCoord = yMax of each row
            newRow = Row(rowName, rowCoord,
                         (rowHeight+rowCoord), rowSub, numSites)
            rowList.append(newRow)  # append every row on the list of rows

    f.close()  # Close .scl file
    """               End of Parse .scl              """

    """
    for i in rowList:
        print(i)
    """
