"""
Evolutionary Biology Simulation
Written by Nathan Diggins
"""

import matplotlib.pyplot as plt
import Evlib as E
import numpy as np

# Use the mode parameter to change which simulation is run.

mode = 1

if mode == 1:
    """
    Test simulation 1:
    In this simulation, the following properties of the program were checked:
        : Population reached carrying capacity
        : Any initial population will decrease or increase to carrying capacity
    Input parameters:
        :turn_std_deviation = 0.15
        :collision_distance = 0.08
        :traits = {"size": [0.00,1], "speed": [0.00,0.05], "sense":[0.00,0.10]}
    """
    species = E.Species('A')
    initial_organisms = [E.Organism((0, 0), species, energy=500) for i in range(1)]
    food_items = [E.Food((0, 0)) for i in range(50)]
    board = E.Board(initial_organisms + food_items, 100)
    datas = []
    for i in range(300):
        board.reset_object_positions()
        while len([k for k in board.organisms if k.hidden == False]) != 0:
            board.update()
        for org in board.organisms:
            org.energy = 500
            if org.food_count > 1:
                org.hidden = False
                org.reproduce(board)
            if org.food_count < 1:
                board.remove(org)
            else:
                org.hidden = False
        print {i: i.food_count for i in board.organisms}
        board.food = [E.Food((0, 0)) for i in range(300)]
        datas.append(board.get_data())

    plt.plot(range(300), [np.average(datas[i]['intel']) for i in range(300)])
    plt.plot(range(300), [datas[i]['N'] for i in range(300)])
    plt.show()
