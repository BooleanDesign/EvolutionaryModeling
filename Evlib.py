"""
Evolutionary Modeling Library
writen by Nathan Diggins (Boolean Design)
"""
import random as r
import matplotlib.pyplot as plt
import numpy as np

"""
Essential Configuration Parameters
"""
turn_std_deviation = 0.2
collision_distance = 0.08


class Object:
    def __init__(self, position):
        """
        Defines the basic object class.
            Inherits to all other classes which are placed on the board.
        :param position: {type tuple}. Specifies the x and y positions of the particles.
        """
        if type(position) != tuple:
            raise SyntaxError
        self.position = position

    def distance(self, other):
        return (other.position[0] - self.position[0]) ** 2 + (other.position[1] - self.position[1]) ** 2

    def __sub__(self, other):
        return (self.position[0] - other.position[0], self.position[1] - other.position[1])


class Species:
    def __init__(self, name):
        self.sp = name


class Organism(Species, Object):
    def __init__(self, position, species, size, speed, sense):
        Species.__init__(self, species)
        Object.__init__(self, position)
        self.direction = 0
        self.sensed_objects = []
        self.intel = sense
        self.size = size
        self.speed = speed
        self.food_count = 0

    def sense_objects(self, board):
        """
        Allows for the organism to sense nearby objects on the board
        :param board: Board within which to search
        :return: {type list} of objects in the sense radius
        """
        # TODO: Check for efficiency
        self.sensed_objects = []  # Clear the sensed objects and work through again
        for obj in board.objects:  # Iterate through the objects on the board to see if any are close.
            dif = obj - self
            if dif[0] ** 2 + dif[1] ** 2 < collision_distance ** 2 and obj.__class__.__name__ == 'Food':  # If object is
                # within grabbing distance
                self.consume(obj, board)
            elif dif[0] ** 2 + dif[
                1] ** 2 < self.intel ** 2 and obj != self:  # If the distance to the object is less than sense...
                self.sensed_objects.append(obj)
            else:
                pass
        return self.sensed_objects

    def update_position(self, board):
        """
        This allows for the organisms to move aboout the board, making decisions about the food they want
        :param board: {type board} this is the input board
        :return:
        """
        objs = self.sense_objects(board)  # Finds all close objects
        if 'Food' not in list(
                set([i.__class__.__name__ for i in objs])):  # Checks if there is or is not food in the radius
            """
            There is no food in the given radius, thus we will direct the organism to move by their speed in a direction
            similar to their current direction.
            """
            valid_point_checker = False
            while valid_point_checker is False:  # This loop is essential to prevent us from leaving the board
                self.direction = (self.direction + r.gauss(0, turn_std_deviation)) % (
                        2 * np.pi)  # gives us a movement position
                if (self.position[0] + (self.speed * np.cos(self.direction)) < board.size - 1 and self.position[
                    1] + (self.speed * np.sin(self.direction)) < board.size - 1) and (
                        self.position[0] + (self.speed * np.cos(self.direction)) > 0 and self.position[
                    1] + (self.speed * np.sin(self.direction)) > 0):
                    """
                    The position is acceptably within the board
                    """
                    self.position = (self.position[0] + self.speed * np.cos(self.direction),
                                     self.position[1] + self.speed * np.sin(self.direction))

                    valid_point_checker = True  # Allows the loop to break
                else:
                    pass
        else:
            """
            There is food in the sense area!
            """
            closest_food_values = [self.distance(i) for i in self.sensed_objects]
            closest_food = self.sensed_objects[closest_food_values.index(min(closest_food_values))]
            self.direction = np.arctan2(closest_food.position[1] - self.position[1],
                                        closest_food.position[0] - self.position[0])
            self.position = (self.position[0] + self.speed * np.cos(self.direction),
                             self.position[1] + self.speed * np.sin(self.direction))

    def consume(self, object, board):
        """
        Allows for the consumption of objects
        :param object: {Food type} will be the consumed object
        :param board: {type board} this is the sim board object
        :return: None
        """
        # TODO: Add a organism-organism consumption methodology
        if object.__class__.__name__ != 'Food':  # If the object isn't food.
            return None
        else:
            print 'FOOD!'
            self.food_count += 1
            board.remove(object)
            return None


class Food(Object):
    def __init__(self, position):
        Object.__init__(self, position)
        # TODO: Write full Food class
        return None


class Board:
    def __init__(self, objects, size):
        """
        Defines the simulation board
        :param objects: {type list} should include all objects on the board
        :param size: {type int} specifies the size of the board.
        """
        if type(size) != int:
            raise SyntaxError
        if type(objects) != list:
            raise SyntaxError
        self.size = size
        self.objects = objects
        self.food = [i for i in self.objects if i.__class__.__name__ == 'Food']
        self.organisms = [i for i in self.objects if i.__class__.__name__ == 'Organism']
        self.x, self.y = np.meshgrid(np.arange(0, size, 1),
                                     np.arange(0, size, 1))  # Defines the grid as an array of size (size)
        """
        Creating all of the points on the border of the board. Utilized for object placement.
        """
        self.border = list(
            set([(self.x[0][i], self.y[0][i]) for i in range(self.size)] + [(self.x[:, -1][i], self.y[:, -1][i]) for i
                                                                            in range(self.size)] + [
                    (self.x[-1][i], self.y[-1][i]) for i in range(self.size)] + [(self.x[:, 0][i], self.y[:, 0][i])
                                                                                 for i in range(self.size)]))

    def update(self):
        for org in self.organisms:
            org.update_position(self)

    def remove(self, object):
        """
        Removes an object from the board
        :param object: {class object}
        :return: None
        """
        if object not in self.objects:
            raise ValueError
        self.objects.remove(object)
        return None

    def append(self, object):
        """
        Allows for the addition of an object to the board
        :param object: {class object}
        :return: None
        """
        try:
            self.objects.append(object)
            return None
        except:
            raise ValueError

    def reset_object_positions(self):
        """
        Used to reset the board after each repitition
        :return: None
        """
        temp_borders = self.border[:]
        try:
            for obj in self.objects:
                # Rotate through each of the objects in the board
                if obj.__class__.__name__ == "Organism":
                    """
                    This instance of obj is an Organism, thus place on the border
                    """
                    obj.position = temp_borders.pop(r.randint(0, len(temp_borders) - 1))
                    """
                    Now we have to determine which way to make the organism face
                    """
                    if obj.position[0] == 0 and (obj.position[1] != 0 and obj.position[1] != self.size):
                        """
                        The object is on the bottom
                        """
                        obj.direction = np.pi / 2.0
                    elif obj.position[0] == self.size and (obj.position[1] != 0 and obj.position[1] != self.size):
                        """
                        The object is on the top
                        """
                        obj.direction = 3 * np.pi / 2
                    elif obj.position[1] == 0 and (obj.position[0] != 0 and obj.position[0] != self.size):
                        """
                        The object is on the left
                        """
                        obj.direction = 0
                    elif obj.position[1] == self.size and (obj.position[0] != 0 and obj.position[0] != self.size):
                        """
                        The object is on the right
                        """
                        obj.direction = np.pi
                    elif obj.position == (0, 0):
                        obj.direction = np.pi / 4.0
                    elif obj.position == (0, self.size):
                        obj.direction = np.pi * (7.0 / 4.0)
                    elif obj.position == (self.size, self.size):
                        obj.direction = np.pi * (5.0 / 4.0)
                    else:
                        obj.direction = np.pi * (6.0 / 8.0)
                elif obj.__class__.__name__ == "Food":
                    """
                    This is a food object
                    """
                    # TODO: This allows for overlapping food objects... Is that okay?
                    obj.position = (self.x[0][r.randint(1, self.size - 2)], self.y[r.randint(1, self.size - 2)][0])
                else:
                    raise TypeError
        except:
            raise TypeError

    def generate_plot(self, figure):
        """
        Generates a plot of the board
        :param figure: {plt.axes type}
        :return: None
        """
        try:
            board_axes = figure.add_subplot(111)
            board_axes.plot([0, self.size - 1, self.size - 1, 0, 0], [0, 0, self.size - 1, self.size - 1, 0], 'r',
                            linewidth=4)  # Plot the borders
            board_axes.plot([i.position[0] for i in self.objects if i.__class__.__name__ == 'Organism'],
                            [i.position[1] for i in self.objects if i.__class__.__name__ == 'Organism'], 'bx')
            board_axes.plot([i.position[0] for i in self.objects if i.__class__.__name__ == 'Food'],
                            [i.position[1] for i in self.objects if i.__class__.__name__ == 'Food'], 'go')
        except:
            raise ValueError


fig1 = plt.figure()
nate = Species('Nate')
objs = [Organism((r.randint(1, 10), r.randint(1, 10)), nate, 1, 0.1, 1.0)] + [
    Food((r.randint(1, 10), r.randint(1, 10))) for i in range(25)]
B = Board(objs, 11)
B.reset_object_positions()
pos = []
for q in range(300):
    B.update()
    pos.append(B.organisms[0].position)

x = [i[0] for i in pos]
y = [i[1] for i in pos]
B.generate_plot(fig1)
plt.plot(x, y)
plt.show()
