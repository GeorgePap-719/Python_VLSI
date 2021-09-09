class Design:

    def __init__(self, num_of_cells, num_of_terminals, num_of_nets):
        self.density = None
        self.num_of_cells = num_of_cells
        self.num_of_terminals = num_of_terminals
        self.num_of_nets = num_of_nets
        self.width = None
        self.height = None
        self.total_area = None
        self.total_cell_area = None
        self.half_perimeter_wirelength = None

    def calculate_design_width_height(self):
        pass

    def calculate_design_density(self):
        pass

    def calculate_design_total_area(self):
        pass

    def calculate_design_total_cell_area(self, node_list):
        # total_cell_area = 0
        # for node in node_list:
        pass

    def calculate_design_half_perimeter_wirelength(self, net_list):
        total_hpw = 0

        for net in net_list:
            total_hpw += net.wirelength

        self.half_perimeter_wirelength = int(total_hpw)

    def __str__(self):
        return (str(self.density) + " " + str(self.num_of_cells)
                + " " + str(self.num_of_terminals)
                + " " + str(self.num_of_nets)
                + " " + str(self.width) + " " + str(self.height)
                + " " + str(self.total_area) + " " + str(self.total_cell_area)
                + " " + str(self.half_perimeter_wirelength))
