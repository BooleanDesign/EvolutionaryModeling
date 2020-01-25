"""
Evolutionary Modeling Library
writen by Nathan Diggins (Boolean Design)
"""
import random as r

import numpy as np


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


class Species:
    def __init__(self):
        # TODO: Write full species class.
        return None


class Organism(Species, Object):
    def __init__(self):
        # TODO: Write full organism class
        return None


class Food(Object):
    def __init__(self):
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

    def remove_object(self, object):
        """
        Removes an object from the board
        :param object: {class object}
        :return: None
        """
        if object not in self.objects:
            raise ValueError
        self.objects.remove(object)
        return None

    def add_object(self, object):
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
                elif obj.__class__.__name__ == "Food":
                    """
                    This is a food object
                    """
                    # TODO: This allows for overlapping food objects... Is that okay?
                    obj.position = (self.x[0][r.randint(0, self.size - 1)], self.y[r.randint(0, self.size - 1)][0])
                else:
                    raise TypeError
        except:
            raise TypeError
