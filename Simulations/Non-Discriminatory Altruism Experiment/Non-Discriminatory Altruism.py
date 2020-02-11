"""
Population Growth Valitation Test: Population growth under food scarcity.
Written by: Nathan Diggins
"""
import Evlib as E
import matplotlib.pyplot as plt
import numpy as np

data_file = open('Trial 1.csv', 'w+')  # Opens Trial 1.csv as the main datafile
# Set up the simulation with 1 organism and 45 food items
species = E.Species('A')
initial_organisms = [E.Organism((0, 0), species, energy=1000) for i in range(18)] + [
    E.Organism((0, 0), species, energy=1000, altruism=True) for i in range(18)]
food_items = [E.Food((0, 0)) for i in range(45)]
full_data = []

"""
Run the simulation
"""
ARP = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
for w in range(5):
    E.ARP = 1.0
    species = E.Species('A')
    initial_organisms = [E.Organism((0, 0), species, energy=1000) for i in range(18)] + [
        E.Organism((0, 0), species, energy=1000, altruism=True) for i in range(18)]
    food_items = [E.Food((0, 0)) for i in range(45)]
    board = E.Board(initial_organisms + food_items, 20)
    d = [board.get_data()]
    for k in range(30):
        print w, k, d[k]['NA'], E.ARP
        h = board.run_day(45)
        d.append(h)
    full_data.append(d)

for test in full_data:
    data_file.write('Test: ' + str(full_data.index(test) + 1) + '\n')
    max_data = max([len(b['speed']) for b in test])  # This is the number of altruists
    for t in test:
        data_file.write(str(t["N"]) + ',')
        for org in t["AT POP"]:
            data_file.write(str(org) + ',')
        data_file.write((max_data - len(t['speed'])) * ' ,')
        data_file.write(
            str(t["NA"]) + ',' + str(t['NE']) + ',' + str(float(t["NA"]) / float(t['N'])) + ',' + str(
                float(t["NE"]) / float(t['N'])) + '\n')
data_file.close()
