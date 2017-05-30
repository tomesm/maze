import numpy
#rom numpy.random import random_integers as rand

cimport numpy
cimport cython

cdef extern from "stdlib.h":
    int rand()
    void srand(long int seedval)


cdef extern from "time.h":
    long int time(int)


cdef int randint(int limit):
    return rand() % limit

def generate_maze(int width=81, int height=51, double complexity=0.75, double density=0.75):
    """ Convert the maze to required format """
    # We ned walls marked as negative numbers so we need to re-type the base
    maze = generate_base_maze(width, height, complexity, density).astype(int)
    # rewrite walls as -1
    maze[maze == 1] = -1
    # non-negatives (zeros in this case) are cells so no need to customize
    # set target at random cell
    cells = numpy.where(maze == 0)
    target = numpy.random.randint(0, len(cells[0]))
    # set target coordinates inside sells arrays
    target_x = cells[0][target]
    target_y = cells[1][target]
    maze[target_x, target_y] = 1
    return maze


cpdef numpy.ndarray[numpy.int8_t, ndim=2] generate_base_maze(int width=81, int height=51, double complexity=0.75, double density=0.75):
    """ Let's just re-use a generator from Wikipeida:

            Source: https://en.wikipedia.org/wiki/Maze_generation_algorithm
            License: Creative Commons Attribution-ShareAlike 3.0 Unported License
            https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License
    """
    # Only odd shapes
    cdef numpy.ndarray[numpy.int_t, ndim=1] shape = numpy.empty(2, dtype=numpy.int)
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    cdef int icomplexity = int(complexity * (5 * (shape[0] + shape[1])))
    cdef int idensity = int(density * ((shape[0] // 2) * (shape[1] // 2)))
    # Build actual maze
    cdef numpy.ndarray[numpy.int8_t, ndim=2] Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles
    for i in range(idensity):
        x, y = randint(shape[1] // 2) * 2, randint(shape[0] // 2) * 2
        Z[y, x] = 1
        for j in range(icomplexity):
            neighbours = []
            if x > 1:
                neighbours.append((y, x - 2))
            if x < shape[1] - 2:
                neighbours.append((y, x + 2))
            if y > 1:
                neighbours.append((y - 2, x))
            if y < shape[0] - 2:
                neighbours.append((y + 2, x))
            if len(neighbours):
                y_, x_ = neighbours[randint(len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return Z

