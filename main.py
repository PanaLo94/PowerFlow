import CreateGrid
import pandapower as pp
import pandas as pd


# creating a pre-loaded grid
def createStandardGrid():
    print('This grid is auto generated')
    net = pp.create_empty_network()

    min_vm_pu = .95
    max_vm_pu = 1.05

    bus = []
    g = []
    line = []

    # create buses
    for i in range(3):
        bus.append(pp.create_bus(net, vn_kv=110., min_vm_pu=min_vm_pu, max_vm_pu=max_vm_pu))

    # create lines
    for i in range(3):
        if i != 2:
            line.append(pp.create_line(net, bus[i], bus[i + 1], length_km=1., std_type='149-AL1/24-ST1A 110.0'))
        else:
            line.append(pp.create_line(net, bus[i], bus[0], length_km=1., std_type='149-AL1/24-ST1A 110.0'))

    # create load
    pp.create_load(net, bus[2], p_mw=300)

    # create generators
    for i in range(2):
        if i != 1:
            g.append(pp.create_gen(net, bus[i], p_mw=200, min_p_mw=0, max_p_mw=300, controllable=True, slack=True))
        else:
            g.append(pp.create_gen(net, bus[i], p_mw=0, min_p_mw=0, max_p_mw=300, controllable=True))

    print(net)

    return net, g


# calculate optimal power flow
def action(net, g, generator_prices):
    for i in range(len(g)):
        pp.create_poly_cost(net, element=g[i], et="gen", cp1_eur_per_mw=generator_prices[i])

    pp.runopp(net)
    print(net.res_gen)
    df = pd.DataFrame(net.res_gen)
    df.to_csv('optimal_flow.csv', index=False)


def main():
    #Manual input grid #1

    # bus_counter = 3
    #
    # line_counter = 3
    # line_connections = [[0, 1], [1, 2], [2, 0]]
    #
    # load_positions = [2]
    # load_power = [300]
    #
    # generator_positions = [0, 1]
    # generator_pmx = [200, 0]
    # generator_pmin = [0, 0]
    # generator_pmax = [300, 300]
    # generator_prices = [30, 25]

    #Manual input grid #2
    bus_counter = 4

    line_counter = 6
    line_connections = [[0, 3], [2, 3], [1, 3], [0, 1], [0, 2], [1, 2]]

    load_positions = [3]
    load_power = [300]

    generator_positions = [0, 1, 2]
    generator_pmx = [200, 200, 200]
    generator_pmin = [0, 0, 0]
    generator_pmax = [300, 300, 300]
    generator_prices = [30, 25, 24]

    testGrid = CreateGrid.createGrid(bus_counter, generator_positions, load_positions, line_counter, generator_pmx,
                                     generator_pmin, generator_pmax, load_power, line_connections)

    selection = input('For an auto generated grid choose "a" and for a manual choose "b" ')
    if selection == 'a':
        netAuto, gAuto = createStandardGrid()
        action(netAuto, gAuto, generator_prices=[30, 30])
    elif selection == 'b':
        netManual, gManual = testGrid.createManualGrid()
        action(netManual, gManual, generator_prices)
    else:
        print('Cant recognize input.')


if __name__ == '__main__':
    main()
