"""
Evolutionary Modeling Library
writen by Nathan Diggins (Boolean Design)
"""
import random as r
import matplotlib.pyplot as plt
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
    def __init__(self,name):
        self.sp = name





class Organism(Species, Object):
    def __init__(self,position,species,size,speed,sense):
        Species.__init__(self,species)
        Object.__init__(self,position)
        self.intel = sense
        self.size = size
        self.speed = speed



class Food(Object):
    def __init__(self,position):
        Object.__init__(self,position)
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

    def generate_plot(self,figure):
        """
        Generates a plot of the board
        :param figure: {plt.axes type}
        :return: None
        """
        try:
            board_axes = figure.add_subplot(111)
            board_axes.plot([0,self.size-1,self.size-1,0,0],[0,0,self.size-1,self.size-1,0],'r',linewidth=4) #Plot the borders
            board_axes.plot([i.position[0] for i in self.objects if i.__class__.__name__ == 'Organism'],
                            [i.position[1] for i in self.objects if i.__class__.__name__ == 'Organism'],'bx')
            board_axes.plot([i.position[0] for i in self.objects if i.__class__.__name__ == 'Food'],
                            [i.position[1] for i in self.objects if i.__class__.__name__ == 'Food'], 'go')
        except:
            raise ValueError


fig1 = plt.figure()
objs = [Organism((r.randint(1,10),r.randint(1,10))) for i in range(20)]+[Food((r.randint(1,10),r.randint(1,10))) for i in range(25)]
B = Board(objs,11)
B.reset_object_positions()
B.generate_plot(fig1)
plt.show()