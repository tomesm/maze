import numpy
import copy
from numpy.random import random_integers as rand
import matplotlib.pyplot as pyplot
from .generator import generate_maze

class Solution():
    """
        Maze solution object
    """
    def __init__(self, maze):
        self.maze = maze
        self.distances = self.maze[:, :, 0]
        self.directions = self.maze[:, :, 1]
        self.is_reachable = ' ' not in self.maze[:, :, 1]


    def path(self, row, column):
        """ """
        if self.maze[row, column, 1] == '#' or\
                self.maze[row, column, 1] == ' ':
            raise Exception("Cell not reachable.")

        path = []
        coordinates = (row, column)
        while self.maze[coordinates][1] != 'X':
            path.append(coordinates)
            if self.maze[coordinates][1] == '>':
                coordinates = (coordinates[0], coordinates[1]+1)
            elif self.maze[coordinates][1] == '<':
                coordinates = (coordinates[0], coordinates[1]-1)
            elif self.maze[coordinates][1] == '^':
                coordinates = (coordinates[0]-1, coordinates[1])
            elif self.maze[coordinates][1] == 'v':
                coordinates = (coordinates[0]+1, coordinates[1])
        path.append(coordinates)
        return path



def analyze(array):
    # create array of ASCII bytes
    maze = numpy.empty(shape=(array.shape[0], array.shape[1], 2), dtype="<U15")
    # fill the ASCII maze:
    # fill walls
    maze[(array == -1, 1)] = '#'
    # fill paths
    maze[(array == 0, 1)] = ' '
    # set target
    maze[(array == 1, 1)] = 'X'
    # add default distances which marke all cells as not visited in the same
    # time
    maze[:, :, 0] = '-1'
    # implementing Breadth-first algorithm, starting at target
    # get location of target
    target = numpy.where(maze == 'X')[:2]
    # start traveling through maze
    starting_cell = numpy.transpose(target)
    while len(starting_cell):
        current_cell = starting_cell
        starting_cell = []
        for coordinates in current_cell:
            # get cell coordinates
            cell = maze[coordinates[0], coordinates[1]]
            # get surrounding cells positions
            cell_up = (coordinates[0]-1, coordinates[1])
            cell_down = (coordinates[0]+1, coordinates[1])
            cell_right = (coordinates[0], coordinates[1]+1)
            cell_left = (coordinates[0], coordinates[1]-1)
            # now we check surrounding cells if they were visited before and
            # are not walls in the same time
            # first, try go up
            if (maze[cell_up][1] == ' ' and  # is a path
                    maze[cell_up][0] == '-1'
               ):  # and not visited before
                maze[cell_up][1] = 'v' # set direction
                maze[cell_up][0] = str(int(cell[0]) + 1) # compute distance
                starting_cell.append(list(cell_up))
            # try go down
            if (maze[cell_down][1] == ' ' and
                    maze[cell_down][0] == '-1'
               ):
                maze[cell_down][1] = '^'
                maze[cell_down][0] = str(int(cell[0]) + 1)
                starting_cell.append(list(cell_down))
            # try go left
            if (maze[cell_left][1] == ' ' and
                    maze[cell_left][0] == '-1'
               ):
                maze[cell_left][1] = '>'
                maze[cell_left][0] = str(int(cell[0]) + 1)
                starting_cell.append(list(cell_left))
            # try go right
            if (maze[cell_right][1] == ' ' and
                    maze[cell_right][0] == '-1'
               ):
                maze[cell_right][1] = '<'
                maze[cell_right][0] = str(int(cell[0]) + 1)
                starting_cell.append(list(cell_right))
    return Solution(maze)
