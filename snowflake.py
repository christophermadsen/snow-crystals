""" Snowflake modelling
Snowflakes are formed with diffusion limited aggregation
this can be modelled using cellular automata with a
hexagonal grid. """

import matplotlib.pyplot as plt
import random
import pyglet
import numpy as np

""" Starting condition:
St(z) is state (amount of water content) for cell z at time t
Beta is fixed constant of background vapor level (between 0 - 1)"""

class Snowflake_Model:

    def __init__(self, window_width, window_height, cell_size, alpha, beta, gamma):
        self.grid_width = int(window_width / cell_size)
        self.grid_height = int(window_height / cell_size)
        self.cell_size = cell_size
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.cells = []
        self.generate_cells()


    def generate_cells(self):
        for row in range(0, self.grid_height):
            self.cells.append([])
            for col in range(0, self.grid_width):
                # to test if grid is working (needs to be one filled ofc)
                if row == int(self.grid_height/2) and col == int(self.grid_height/2):
                    self.cells[row].append(1)
                    grid[({}, {}).format(row, col)] = Cell(0, 0, 1)
                else:
                    self.cells[row].append(0)
                    grid[({}, {}).format(row, col)] = Cell(0, 0, self.beta)

    def if_receptive(self):
        neighbours = get_neigbours(grid, hexagon)
        for qr in neighbours:
            state = get_cell_value(qr[0], qr[1])
            if state == 1:
                return True
        return False

    def umean_neigbours(self):
        u_values = []
        for qr in get_neighbours(grid hexagon):
            u_values.append(get_cell_value(qr[0], qr[1])))
        return sum(u_values)/len(u_values)

    def run_rules(self):
        """ Rules that update cells """
        pass
        for row in range(0, self.grid_height):
            for col in range(0, self.grid_width):
                if if_receptive(self):
                    self.u = 0
                    self.v = self.state
                else:
                    self.u = self.state
                    self.v = 0

        for row in range(0, self.grid_height):
            for col in range(0, self.grid_width):
                u = self.u + self.alpha/2 * (umean_neighbours(self) - self.u)
                v = self.v + self.gamma
            self.state = self.u + self.v
            Cell(row, col, self.u, sefl.v, self.state)

    def get_cell_value(self, row, col):
        """ Returning value of one cell """
        pass


    def draw(self):

        for row in range(0, self.grid_height):
            for col in range(0, self.grid_width):
                if self.cells[row][col] == 1:
                    hex_coords = (
                    int(row * self.cell_size - self.cell_size / 2), int(col * self.cell_size  - (self.cell_size/2) / np.sin(np.deg2rad(60))),
                    int(row * self.cell_size - self.cell_size / 2), int(col *  self.cell_size +  (self.cell_size/2) / np.sin(np.deg2rad(60))),
                    int(row * self.cell_size),                      int(col *  self.cell_size + self.cell_size / 2),
                    int(row * self.cell_size + self.cell_size / 2), int(col *  self.cell_size +  (self.cell_size/2) / np.sin(np.deg2rad(60))),
                    int(row * self.cell_size + self.cell_size / 2), int(col *  self.cell_size -  (self.cell_size/2) / np.sin(np.deg2rad(60))),
                    int(row * self.cell_size),                      int(col *  self.cell_size - self.cell_size / 2),
                    int(row * self.cell_size),                      int(col *  self.cell_size))



                    pyglet.graphics.draw_indexed(7, pyglet.gl.GL_TRIANGLES,
                                                [0, 1, 6, 1, 2, 6, 2, 3, 6,
                                                3, 4, 6, 4, 5, 6, 0, 5, 6],
                                                ('v2i', hex_coords))

    class Cell:
        def __init__(self, u, v, state):
            self.u = u
            self.v = v
            self.state = state
