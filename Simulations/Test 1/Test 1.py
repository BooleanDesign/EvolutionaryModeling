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
initial_organisms = [E.Organism((0, 0), species, energy=1000) for i in range(1)]
food_items = [E.Food((0, 0)) for i in range(45)]
full_data = []
marks = ['.', '1', 'x', '4', '_']
q = 0.80643
"""
Run the simulation
"""
for w in range(5):
    species = E.Species('A')
    initial_organisms = [E.Organism((0, 0), species, energy=1000) for i in range(1)]
    food_items = [E.Food((0, 0)) for i in range(45)]
    board = E.Board(initial_organisms + food_items, 20)
    d = [board.get_data()]
    for k in range(30):
        print w, k, d[k]['N']
        h = board.run_day(45)
        d.append(h)
    full_data.append(d)

plt.figure()
for i in range(5):
    plt.plot(range(31), [full_data[i][j]['N'] for j in range(31)], 'k%s' % (marks[i]), label='Trial %s' % (str(i + 1)))

plt.plot(range(31), [np.average([full_data[i][j]['N'] for i in range(5)]) for j in range(31)], 'k:', linewidth=2,
         label=r'$\bar{P}$')
plt.plot(range(31), [(36.0) / (1 + np.e ** (-1 * q * (y - (np.log(35.0) / q)))) for y in range(31)], 'k--',
         label='Theoretical')
plt.title('Population Growth Under Food Scarcity')
plt.xlabel('Generation')
plt.ylabel('Organisms')
plt.legend(loc='upper left')
for test in full_data:
    data_file.write(str(full_data.index(test) + 1) + ',')
    for t in test[:-1]:
        data_file.write(str(t["N"]) + ',')
    data_file.write(str(test[-1]['N']) + '\n')

data_file.close()
plt.show()
