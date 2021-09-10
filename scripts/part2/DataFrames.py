import pandas as pd
from pandas import DataFrame

pd.set_option('display.width', 800)
pd.set_option('display.max_columns', 20)


# Nodes DataFrame & functions for it
def create_nodes_df(node_list):

    nodes_df = pd.DataFrame.from_records([node.to_dict() for node in node_list])
    nodes_df['Size'] = nodes_df["Width"] * nodes_df["Height"]

    nodes_df.loc[nodes_df['Type'] == 'Terminal', 'Coordinate_x_max'] = (
        nodes_df['Coordinate_x_min'])
    nodes_df.loc[nodes_df['Type'] == 'Non_Terminal', 'Coordinate_x_max'] = (
         nodes_df['Coordinate_x_min'] + nodes_df['Width'])

    nodes_df.loc[nodes_df['Type'] == 'Terminal', 'Coordinate_y_max'] = (
        nodes_df['Coordinate_y_min'])
    nodes_df.loc[nodes_df['Type'] == 'Non_Terminal', 'Coordinate_y_max'] = (
            nodes_df['Coordinate_y_min'] + nodes_df['Height'])

    nodes_df = nodes_df.astype({"Coordinate_x_max": int,
                                "Coordinate_y_max": int})

    return nodes_df


def biggest_non_terminal_node(nodes_df):

    max_df = nodes_df[nodes_df['Type'].str.match('Non_Terminal')]
    max_node_size = int(max_df['Size'].max())

    max_df = max_df[max_df.Size == max_node_size]
    max_nodes_list = list(max_df.Node_name)

    print("Maximum Non Terminal Node size = ", max_node_size)
    print("- Non Terminal Node(s) with max size: ", max_nodes_list)
    # print("\n")


def smallest_non_terminal_node(nodes_df):

    min_df = nodes_df[nodes_df['Type'].str.match('Non_Terminal')]
    min_node_size = int(min_df['Size'].min())

    min_df = min_df[min_df.Size == min_node_size]
    min_nodes_list = list(min_df.Node_name)

    # print(min_df.get(["Node_name", "Size"]).to_string(index=False))
    print("Minimum Non Terminal Node size = ", min_node_size)
    print("- Non Terminal Node(s) with min size: ", min_nodes_list)
    # print("\n")


def mean_size_non_terminal_nodes(nodes_df):

    mean_df = nodes_df[nodes_df['Type'].str.match('Non_Terminal')]
    mean = float(mean_df['Size'].mean())
    mean = round(mean, 2)

    print("Mean size of Non Terminal Node(s): ", mean)


def node_with_most_connections(nodes_df, nets_df):

    temp_df = nodes_df[nodes_df['Type'].str.match('Non_Terminal')]
    node_list = list(temp_df['Node_name'])
    nets_node_list = list(nets_df['Nodes'])

    flag = True
    max_connections = None
    max_node = None

    for node_name in node_list:
        connections = set()   # set, to avoid duplicate connections
        for row in nets_node_list:
            for elem in row:
                if node_name == elem:
                    connections.update(row)

        # (len of set) - 1 = connections of a node.
        # We decrease by one, cause in the set it's also the name of the node
        # that we each time look for its connections. So we don't count it
        # as a connection with itself.
        if flag:
            max_connections = len(connections) - 1
            max_node = node_name
            flag = False
        elif max_connections < len(connections) - 1:
            max_connections = len(connections) - 1
            max_node = node_name

    print("Cell " + str(max_node) + " has the most connections = "
          + str(max_connections))


def node_with_least_connections(nodes_df, nets_df):

    temp_df = nodes_df[nodes_df['Type'].str.match('Non_Terminal')]
    node_list = list(temp_df['Node_name'])
    nets_node_list = list(nets_df['Nodes'])

    flag = True
    min_connections = None
    min_node = None

    for node_name in node_list:
        connections = set()   # set, to avoid duplicate connections
        for row in nets_node_list:
            for elem in row:
                if node_name == elem:
                    connections.update(row)

        # (len of set) - 1 = connections of a node.
        # We decrease by one, cause in the set it's also the name of the node
        # that we each time look for its connections. So we don't count it
        # as a connection with itself.
        if flag:
            min_connections = len(connections) - 1
            min_node = node_name
            flag = False
        elif min_connections > len(connections) - 1:
            min_connections = len(connections) - 1
            min_node = node_name

    print("Cell " + str(min_node) + " has the least connections = "
          + str(min_connections))


def mean_number_of_node_connections(nodes_df, nets_df):
    temp_df = nodes_df[nodes_df['Type'].str.match('Non_Terminal')]
    node_list = list(temp_df['Node_name'])
    nets_node_list = list(nets_df['Nodes'])

    total_connections = 0

    for node_name in node_list:
        connections = set()   # set, to avoid duplicate connections
        for row in nets_node_list:
            for elem in row:
                if node_name == elem:
                    connections.update(row)

        total_connections += len(connections) - 1

    mean_connections = total_connections / len(nodes_df)
    mean_connections = round(mean_connections,2)
    print("Mean connections of design cells: ", mean_connections)


# Nets DataFrame & functions for it
def create_nets_df(net_list, nodes_df):

    nets_df = pd.DataFrame.from_records([net.to_dict() for net in net_list])

    find_min_max_on_nets_df(nodes_df, nets_df)
    calculate_net_hpw(nets_df)
    calculate_net_size(nets_df)
    nets_df = nets_df.astype({"Half_Perimeter_Wirelength": int, "Net_Size": int})
    nets_df = nets_df.astype({"Coordinate_x_min": int, "Coordinate_x_max": int,
                              "Coordinate_y_min": int, "Coordinate_y_max": int})

    return nets_df


def find_min_max_on_nets_df(nodes_df, nets_df):
    net_names_list = list(nets_df['Net_name'])
    net_externals_list = list(nets_df['External_nodes'])
    print("\n")

    x_max = None
    x_min = None
    y_max = None
    y_min = None

    for net_name, node_names in zip(net_names_list, net_externals_list):

        flag = 0
        for name in node_names:
            if flag == 0:
                flag += 1
                x_max = int(nodes_df.loc[nodes_df['Node_name'] == name, 'Coordinate_x_max'])
                x_min = int(nodes_df.loc[nodes_df['Node_name'] == name, 'Coordinate_x_min'])
                y_max = int(nodes_df.loc[nodes_df['Node_name'] == name, 'Coordinate_y_max'])
                y_min = int(nodes_df.loc[nodes_df['Node_name'] == name, 'Coordinate_y_min'])
            else:
                if x_max < int(nodes_df.loc[nodes_df['Node_name'] == name, 'Coordinate_x_max']):
                    x_max = int(nodes_df.loc[nodes_df['Node_name'] == name, 'Coordinate_x_max'])

                if x_min > int(nodes_df.loc[nodes_df['Node_name'] == name, 'Coordinate_x_min']):
                    x_min = int(nodes_df.loc[nodes_df['Node_name'] == name, 'Coordinate_x_min'])

                if y_max < int(nodes_df.loc[nodes_df['Node_name'] == name, 'Coordinate_y_max']):
                    y_max = int(nodes_df.loc[nodes_df['Node_name'] == name, 'Coordinate_y_max'])

                if y_min > int(nodes_df.loc[nodes_df['Node_name'] == name, 'Coordinate_y_min']):
                    y_min = int(nodes_df.loc[nodes_df['Node_name'] == name, 'Coordinate_y_min'])

                # print(x_max, x_min, y_max, y_min)

        nets_df.loc[nets_df['Net_name'] == net_name, 'Coordinate_x_min'] = x_min
        nets_df.loc[nets_df['Net_name'] == net_name, 'Coordinate_x_max'] = x_max
        nets_df.loc[nets_df['Net_name'] == net_name, 'Coordinate_y_min'] = y_min
        nets_df.loc[nets_df['Net_name'] == net_name, 'Coordinate_y_max'] = y_max


def calculate_net_hpw(nets_df):

    nets_df['Half_Perimeter_Wirelength'] = ((nets_df['Coordinate_x_max'] - nets_df['Coordinate_x_min'])
                                    + (nets_df['Coordinate_y_max'] - nets_df['Coordinate_y_min']))


def calculate_net_size(nets_df):

    nets_df['Net_Size'] = ((nets_df['Coordinate_x_max'] - nets_df['Coordinate_x_min'])
                           * (nets_df['Coordinate_y_max'] - nets_df['Coordinate_y_min']))


def biggest_net_based_on_nodes(nets_df):

    max_num_of_cells = int(nets_df["Nodes"].str.len().max())
    max_nets_df = nets_df[nets_df.Nodes.str.len() == max_num_of_cells]
    max_nets_list = list(max_nets_df.Net_name)

    print("Maximum number of cells in a net: ", max_num_of_cells)
    print("- Biggest net(s): ", max_nets_list)
    # print("\n")


def smallest_net_based_on_nodes(nets_df):

    min_num_of_cells = int(nets_df["Nodes"].str.len().min())
    min_nets_df = nets_df[nets_df.Nodes.str.len() == min_num_of_cells]
    min_nets_list = list(min_nets_df.Net_name)

    print("Minimum number of cells in a net: ", min_num_of_cells)
    print("- Smallest net(s): ", min_nets_list)
    # print("\n")


# Rows DataFrame & functions for it
def create_rows_df(row_list, nodes_df):

    rows_df = pd.DataFrame.from_records([row.to_dict() for row in row_list])

    rows_df['Width'] = rows_df['Coordinate_x_max'] - rows_df['Coordinate_x_min']
    rows_df['Height'] = rows_df['Coordinate_y_max'] - rows_df['Coordinate_y_min']
    rows_df['Row_area'] = rows_df['Width'] * rows_df['Height']

    row_density(nodes_df, rows_df)
    rows_df = rows_df.astype({"Nodes_area": int})

    return rows_df


# Find each Row's all nodes_area and then Row density
def row_density(nodes_df, rows_df):

    row_names_list = list(rows_df['Row_name'])

    for row_name in row_names_list:

        # sum of all node_sizes that belong to the current row
        nodes_area = nodes_df[nodes_df.Row_number == row_name].Size.sum()

        # set nodes area to the current Row
        rows_df.loc[rows_df['Row_name'] == row_name, 'Nodes_area'] = nodes_area

    rows_df['Density'] = (rows_df['Nodes_area'] / rows_df['Row_area']) * 100


def smallest_row_based_on_density(rows_df):

    min_density = int(rows_df["Density"].min())
    min_rows_df = rows_df[rows_df.Density == min_density]
    min_rows_list = list(min_rows_df.Row_name)

    print("Minimum Row Density: ", min_density)
    print("- Row(s) with min density: ", min_rows_list)
    print("\n")


def biggest_row_based_on_density(rows_df):

    max_density = int(rows_df["Density"].max())
    max_rows_df = rows_df[rows_df.Density == max_density]
    max_rows_list = list(max_rows_df.Row_name)

    print("Maximum Row Density: ", max_density)
    print("- Row(s) with max density: ", max_rows_list)
    print("\n")


def mean_row_density(rows_df):

    mean = float(rows_df['Density'].mean())
    mean = round(mean, 2)

    print("Mean Row Density: ", mean)
    print("\n")


# Design DataFrame & functions for it
def create_design_df(nodes_df, nets_df, rows_df):

    design_cells = nodes_df.shape[0]
    design_nets = nets_df.shape[0]
    design_rows = rows_df.shape[0]
    design_terminals = len(nodes_df[nodes_df['Type'].str.match('Terminal')])
    design_total_cell_area = nodes_df['Size'].sum()

    design_height = (rows_df['Coordinate_y_max'].max()
                     - rows_df['Coordinate_y_min'].min())

    design_width = (rows_df['Coordinate_x_max'].max()
                    - rows_df['Coordinate_x_min'].min())

    design_total_area = design_height * design_width

    # 1st way to calculate design density
    design_density = (design_total_cell_area / design_total_area) * 100

    # 2nd way to calculate design density
    # density = design_df_density(nodes_df, rows_df)

    design_hpw = design_df_half_perimeter_wirelength(nets_df)

    design_dict = {
        'Number_of_cells': design_cells,
        'Number_of_terminals': design_terminals,
        'Number_of_nets': design_nets,
        'Number_of_rows': design_rows,
        'Width': design_width,
        'Height': design_height,
        'Total_Area': design_total_area,
        'Total_Cell_Area': design_total_cell_area,
        'Half_Perimeter_Wirelength': design_hpw,
        'Density(%)': design_density
    }

    # creation of DF design
    design_df = pd.DataFrame.from_records([design_dict])

    return design_df


def design_df_half_perimeter_wirelength(nets_df):

    design_hpw = nets_df['Half_Perimeter_Wirelength'].sum()

    return design_hpw


def design_df_density(nodes_df, rows_df):

    design_height = (rows_df['Coordinate_y_max'].max()
                     - rows_df['Coordinate_y_min'].min())

    design_width = (rows_df['Coordinate_x_max'].max()
                    - rows_df['Coordinate_x_min'].min())

    design_total_area = design_height * design_width
    design_total_cell_area = nodes_df['Size'].sum()
    density = (design_total_cell_area / design_total_area) * 100

    return density


# Swap two cells and update all the DataFrames after the swap
def swap_cells(nodes_df, nets_df, rows_df, design_df):

    cell_1 = input("Give name of the first cell: ")
    cell_2 = input("Give name of the second cell: ")

    # cell_1_x_max = int(nodes_df.loc[nodes_df['Node_name'] == cell_1, 'Coordinate_x_max'])
    # cell_1_y_max = int(nodes_df.loc[nodes_df['Node_name'] == cell_1, 'Coordinate_y_max'])

    cell_1_x_min = int(nodes_df.loc[nodes_df['Node_name'] == cell_1, 'Coordinate_x_min'])
    cell_1_y_min = int(nodes_df.loc[nodes_df['Node_name'] == cell_1, 'Coordinate_y_min'])
    cell_1_width = int(nodes_df.loc[nodes_df['Node_name'] == cell_1, 'Width'])
    cell_1_row = str(nodes_df.loc[nodes_df['Node_name'] == cell_1, 'Row_number'].to_string(index=False))

    # cell_2_x_max = int(nodes_df.loc[nodes_df['Node_name'] == cell_2, 'Coordinate_x_max'])
    # cell_2_y_max = int(nodes_df.loc[nodes_df['Node_name'] == cell_2, 'Coordinate_y_max'])

    cell_2_x_min = int(nodes_df.loc[nodes_df['Node_name'] == cell_2, 'Coordinate_x_min'])
    cell_2_y_min = int(nodes_df.loc[nodes_df['Node_name'] == cell_2, 'Coordinate_y_min'])
    cell_2_width = int(nodes_df.loc[nodes_df['Node_name'] == cell_2, 'Width'])
    cell_2_row = str(nodes_df.loc[nodes_df['Node_name'] == cell_2, 'Row_number'].to_string(index=False))

    nodes_df.loc[nodes_df['Node_name'] == cell_1, 'Coordinate_x_min'] = cell_2_x_min
    nodes_df.loc[nodes_df['Node_name'] == cell_1, 'Coordinate_y_min'] = cell_2_y_min
    nodes_df.loc[nodes_df['Node_name'] == cell_1, 'Coordinate_x_max'] = cell_2_x_min + cell_1_width
    nodes_df.loc[nodes_df['Node_name'] == cell_1, 'Coordinate_y_max'] = cell_2_y_min + 10
    nodes_df.loc[nodes_df['Node_name'] == cell_1, 'Row_number'] = cell_2_row

    nodes_df.loc[nodes_df['Node_name'] == cell_2, 'Coordinate_x_min'] = cell_1_x_min
    nodes_df.loc[nodes_df['Node_name'] == cell_2, 'Coordinate_y_min'] = cell_1_y_min
    nodes_df.loc[nodes_df['Node_name'] == cell_2, 'Coordinate_x_max'] = cell_1_x_min + cell_2_width
    nodes_df.loc[nodes_df['Node_name'] == cell_2, 'Coordinate_y_max'] = cell_1_y_min + 10
    nodes_df.loc[nodes_df['Node_name'] == cell_2, 'Row_number'] = cell_1_row

    print("\nAfter swap: \n")
    print(nodes_df)

    # Updates on Nets: x_min, x_max, y_min, y_max, Internals, Externals,
    #                  HPW, Size
    find_min_max_on_nets_df(nodes_df, nets_df)
    calculate_net_hpw(nets_df)
    calculate_net_size(nets_df)
    nets_df = nets_df.astype({"Half_Perimeter_Wirelength": int, "Net_Size": int})
    nets_df = nets_df.astype({"Coordinate_x_min": int, "Coordinate_x_max": int,
                              "Coordinate_y_min": int, "Coordinate_y_max": int})

    print("\n")
    print(nets_df)

    # Updates on Rows: Cells, Density, Node_Area
    row_density(nodes_df, rows_df)
    print("\n")
    print(rows_df)

    # Updates on Design: HPW, Density
    create_design_df(nodes_df, nets_df, rows_df)
    print("\n")
    print(design_df)


# Insert a new cell
def insert_a_cell(nodes_df, nets_df, rows_df, design_df):

    name = input("Give name of cell: ")
    x_min = int(input("Give lower left x coordinate of cell: "))
    y_min = int(input("Give lower left y coordinate of cell: "))
    width = int(input("Give name of cell width: "))
    x_max = x_min + width
    height = 10
    y_max = y_min + height
    cell_type = "Non_Terminal"
    size = width * height

    nets = []
    while True:
        answer = input("Add a net? (Y/n): ")
        if answer == "Y":
            current_net_name = input("Give net name, that the cell belongs to: ")
            nets.append(current_net_name)
        else:
            break

    row_name = input("Give cell row number: ")

    # Update Nodes_df with the new cell
    line_df = DataFrame({"Node_name": name,
                         "Width": width,
                         "Height": height,
                         "Type": cell_type,
                         "Row_number": row_name,
                         'Nets': [net_name for net_name in nets],
                         'Coordinate_x_min': x_min,
                         'Coordinate_y_min': y_min,
                         'Coordinate_x_max': x_max,
                         'Coordinate_y_max': y_max,
                         'Size': size
                         })

    nodes_df = nodes_df.append(line_df, ignore_index=False)
    print("\nAfter insert: \n")
    print(nodes_df)

    # Updates on Nets: x_min, x_max, y_min, y_max, Internals, Externals,
    #                  HPW, Size
    find_min_max_on_nets_df(nodes_df, nets_df)
    calculate_net_hpw(nets_df)
    calculate_net_size(nets_df)
    nets_df = nets_df.astype({"Half_Perimeter_Wirelength": int, "Net_Size": int})
    nets_df = nets_df.astype({"Coordinate_x_min": int, "Coordinate_x_max": int,
                              "Coordinate_y_min": int, "Coordinate_y_max": int})
    print("\n")
    print(nets_df)

    # Updates on Rows: Cells, Density, Node_Area
    row_density(nodes_df, rows_df)
    print("\n")
    print(rows_df)

    # Updates on Design: HPW, Density
    create_design_df(nodes_df, nets_df, rows_df)
    print("\n")
    print(design_df)
