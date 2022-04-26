import pandapower as pp


class createGrid:
    def __init__(self, bus_counter, generator_positions, load_positions, line_counter, generator_pmx, generator_pmin,
                 generator_pmax, load_power, line_connections):

        self.bus_counter = bus_counter

        self.load_positions = load_positions
        self.load_power = load_power

        self.line_counter = line_counter
        self.line_connections = line_connections

        self.generator_positions = generator_positions
        self.generator_pmx = generator_pmx
        self.generator_pmin = generator_pmin
        self.generator_pmax = generator_pmax

    def createManualGrid(self):
        print('This grid is manually created')
        net = pp.create_empty_network()

        bus = []
        g = []
        load = []
        line = []

        min_vm_pu = .95
        max_vm_pu = 1.05

        # create buses
        for i in range(self.bus_counter):
            bus.append(pp.create_bus(net, vn_kv=110., min_vm_pu=min_vm_pu, max_vm_pu=max_vm_pu))

        # create lines
        for i in range(self.line_counter):
            line.append(pp.create_line(net, bus[self.line_connections[i][0]], bus[self.line_connections[i][1]],
                                       length_km=1., std_type='149-AL1/24-ST1A 110.0'))

        # create loads
        for i in range(len(self.load_positions)):
            load.append(pp.create_load(net, bus[self.load_positions[i]], p_mw=self.load_power[i]))

        # create generators. If statement so just the first generator gets slack True
        for i in range(len(self.generator_positions)):
            if i == 0:
                g.append(pp.create_gen(net, bus[self.generator_positions[i]], p_mw=self.generator_pmx[i],
                                       min_p_mw=self.generator_pmin[i], max_p_mw=self.generator_pmax[i],
                                       controllable=True,
                                       slack=True))
            else:
                g.append(pp.create_gen(net, bus[self.generator_positions[i]], p_mw=self.generator_pmx[i],
                                       min_p_mw=self.generator_pmin[i], max_p_mw=self.generator_pmax[i],
                                       controllable=True))
        print(net)

        return net, g
