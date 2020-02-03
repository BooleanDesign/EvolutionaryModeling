"""
Test 1: Population growth under food scarcity.
Written by: Nathan Diggins
"""
import Evlib as E
import matplotlib.pyplot as plt
import numpy as np

data_file = open('data.csv', 'w+')  # Opens data.csv as the main datafile
# Set up the simulation with 1 organism and 45 food items
species = E.Species('A')
initial_organisms = [E.Organism((0, 0), species, energy=1000) for i in range(35)]
food_items = [E.Food((0, 0)) for i in range(45)]
full_data = []
E.traits['speed'] = (0.01, 1)
"""
Run the simulation
"""
for w in range(5):
    species = E.Species('A')
    initial_organisms = [E.Organism((0, 0), species, energy=1000) for i in range(35)]
    food_items = [E.Food((0, 0)) for i in range(45)]
    board = E.Board(initial_organisms + food_items, 20)
    d = [board.get_data()]
    for k in range(30):
        print w, k, d[k]['mean_speed']
        h = board.run_day(45)
        d.append(h)
    full_data.append(d)

for test in full_data:
    data_file.write('Test: ' + str(full_data.index(test) + 1) + '\n')
    max_data = max([len(b['size']) for b in test])
    for t in test:
        data_file.write(str(t["N"]) + ',')
        for org in t["speed"]:
            data_file.write(str(org) + ',')
        data_file.write((max_data - len(t['speed'])) * ' ,')
        data_file.write(str(t["mean_speed"]) + '\n')
data_file.close()
