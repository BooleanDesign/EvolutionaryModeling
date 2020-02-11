"""
Population Growth Valitation Test: Population growth under food scarcity.
Written by: Nathan Diggins
"""
import Evlib as E
import matplotlib.pyplot as plt
import numpy as np

for trial in range(10):
    data_file = open('Trial %s.csv' % (str(trial + 2)), 'w+')  # Opens Trial 1.csv as the main datafile
    # Set up the simulation with 1 organism and 45 food items
    species = E.Species('A')
    E.Altruistic_discrimination = True
    initial_organisms = [E.Organism((0, 0), species, energy=1000) for i in range(18)] + [
        E.Organism((0, 0), species, energy=1000, altruism=True) for i in range(18)]
    food_items = [E.Food((0, 0)) for i in range(45)]
    full_data = []

    """
    Run the simulation
    """
    for w in range(10):
        E.ARP = 0.1 * (trial + 1)
        species = E.Species('A')
        initial_organisms = [E.Organism((0, 0), species, energy=1000) for i in range(18)] + [
            E.Organism((0, 0), species, energy=1000, altruism=True) for i in range(18)]
        food_items = [E.Food((0, 0)) for i in range(45)]
        board = E.Board(initial_organisms + food_items, 20)
        d = [board.get_data()]
        for k in range(50):
            print w, k, d[k]['NA'], d[k]["NA"] / d[k]["N"]
            h = board.run_day(45)
            d.append(h)
        full_data.append(d)

    max_length = max([max([len(b['speed']) for b in test]) for test in full_data])
    for test in full_data:
        id = full_data.index(test) + 1
        base_string = ''
        for l in range(max_length):
            base_string += '%s,' % (l + 1)
        data_file.write(
            'Trial %s| ARP = %s,' % (str(id + 1), str(E.ARP)) + base_string + 'Alts,Egos,Alt_Freq,Ego_freq' + '\n')
        for t in test:
            data_file.write(str(t["N"]) + ',')
            for org in t["AT POP"]:
                data_file.write(str(org) + ',')
            data_file.write((max_length - len(t['speed'])) * ' ,')
            data_file.write(
                str(t["NA"]) + ',' + str(t['NE']) + ',' + str(float(t["NA"]) / float(t['N'])) + ',' + str(
                    float(t["NE"]) / float(t['N'])) + '\n')
    data_file.close()
