import Evlib as E
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np

Writer = ani.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)


def init():
    """
    This is the initial formulation of the simulation.
    :return: the object
    """
    trait_data = [(0, board.get_data()['N'])]
    global trait_data

    board.reset_object_positions()
    view_axes.plot([0, board.size - 1, board.size - 1, 0, 0], [0, 0, board.size - 1, board.size - 1, 0], 'r',
                   linewidth=4)  # Plot the borders
    view_axes.plot([i.position[0] for i in board.objects if i.__class__.__name__ == 'Organism'],
                   [i.position[1] for i in board.objects if i.__class__.__name__ == 'Organism'], 'bx')
    view_axes.plot([i.position[0] for i in board.objects if i.__class__.__name__ == 'Food'],
                   [i.position[1] for i in board.objects if i.__class__.__name__ == 'Food'], 'go')
    p = view_axes
    return p,


def animate(i):
    # First we have to reset the board objects:
    gen = i + 1
    view_axes.cla()
    print i
    board.food = [i for i in board.objects if i.__class__.__name__ == 'Food']
    board.organisms = [i for i in board.objects if i.__class__.__name__ == 'Organism']
    if len([org for org in board.organisms if org.hidden == False]) != 0:
        """
        While there are still living organisms on the board.
        """
        board.update()
        trait_data.append((gen, board.get_data()['N']))
        view_axes.plot([0, board.size - 1, board.size - 1, 0, 0], [0, 0, board.size - 1, board.size - 1, 0], 'r',
                       linewidth=4)  # Plot the borders
        view_axes.plot([i.position[0] for i in board.objects if i.__class__.__name__ == 'Organism'],
                       [i.position[1] for i in board.objects if i.__class__.__name__ == 'Organism'], 'bx')
        view_axes.plot([i.position[0] for i in board.objects if i.__class__.__name__ == 'Food'],
                       [i.position[1] for i in board.objects if i.__class__.__name__ == 'Food'], 'go')
        view_axes.set_xlim([-1, board.size])
        view_axes.set_ylim([-1, board.size])
        p = view_axes

        return p
    else:
        board.replicate_generation()
        # Show all
        for organism in board.organisms:
            organism.hidden = False
            organism.food_count = 0
            organism.energy = 500
        # replenish food
        for food in board.food:
            board.remove(food)
        board.objects += [E.Food((0, 0)) for i in range(45)]
        init()


figure1 = plt.figure()
view_axes = figure1.add_subplot(111)

species = E.Species('A')
initial_organisms = [E.Organism((0, 0), species, energy=500) for i in range(30)]
food_items = [E.Food((0, 0)) for i in range(45)]
full_data = []
board = E.Board(initial_organisms + food_items, 20)
ani = ani.FuncAnimation(figure1, animate, frames=5000, interval=0.02, init_func=init)
ani.save('test1.mp4', writer=writer)
