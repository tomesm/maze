import numpy
import pytest
from pymaze import generator

@pytest.fixture
def base():
    return generator.generate_base_maze()


@pytest.fixture()
def maze():
    return generator.generate_maze()


def test_shape(base, maze):
    assert maze.shape == base.shape


def test_border_walls(maze):
    assert numpy.all(maze[0, :] == -1)
    assert numpy.all(maze[-1, :] == -1)
    assert numpy.all(maze[:0] == -1)
    assert numpy.all(maze[:, -1] == -1)
