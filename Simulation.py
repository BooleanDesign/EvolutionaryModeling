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
    initial_organisms = [E.Organism((0, 0), species, energy=500) for i in range(30)]
    food_items = [E.Food((0, 0)) for i in range(50)]
    board = E.Board(initial_organisms + food_items, 100)
    datas = []
    fig1 = plt.figure()
    for i in range(300):
        board.run_day(100)
        board.generate_plot(fig1)
        plt.show()
        datas.append(board.get_data())

    plt.plot(range(30), [np.average(datas[i]['intel']) for i in range(300)])
    # plt.plot(range(300), [datas[i]['N'] for i in range(300)])
    plt.show()
