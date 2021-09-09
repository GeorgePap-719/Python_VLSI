import pandas as pd

pd.set_option('display.width', 800)
pd.set_option('display.max_columns', 20)


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

    print(nets_df)


def calculate_net_hpw(nets_df):

    nets_df['Half_Perimeter_Wirelength'] = ((nets_df['x_max'] - nets_df['x_min'])
                                    + (nets_df['y_max'] - nets_df['y_min']))


def calculate_net_size(nets_df):

    nets_df['Net_Size'] = ((nets_df['x_max'] - nets_df['x_min'])
                           * (nets_df['y_max'] - nets_df['y_min']))


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

    rows_df['Density(%)'] = (rows_df['Nodes_area'] / rows_df['Row_area']) * 100


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
    design_density = (design_total_cell_area / design_total_area) * 100

    # TODO CHECK how to calculate density, with function or like above?
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

    # create DF design
    design_df = pd.DataFrame.from_records([design_dict])

    return design_df


def biggest_non_terminal_node(nodes_df):

    max_df = nodes_df[nodes_df['Type'].str.match('Non_Terminal')]
    max_node_size = int(max_df['Size'].max())

    max_df = max_df[max_df.Size == max_node_size]
    max_nodes_list = list(max_df.Node_name)

    # print(max_df.get(["Node_name", "Size"]).to_string(index=False))
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


def smallest_row_based_on_density(rows_df):

    min_density = int(rows_df["Density"].str.len().min())
    min_rows_df = rows_df[rows_df.Density.str.len() == min_density]
    min_rows_list = list(min_rows_df.Row_name)

    print("Minimum Row Density: ", min_density)
    print("- Row(s) with min density: ", min_rows_list)
    # print("\n")


def biggest_row_based_on_density(rows_df):

    max_density = int(rows_df["Density"].str.len().max())
    max_rows_df = rows_df[rows_df.Density.str.len() == max_density]
    max_rows_list = list(max_rows_df.Row_name)

    print("Maximum Row Density: ", max_density)
    print("- Row(s) with max density: ", max_rows_list)
    # print("\n")


def mean_row_density(rows_df):

    mean = float(rows_df['Density'].mean())
    mean = round(mean, 2)

    print("Mean Row Density: ", mean)


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
