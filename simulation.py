"""
.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.
Authors:                                                                    *
    Fenna Houtsma, Christopher Buch Madsen, Guido Vaessen                   *
                                                                            *
Date:                                                                       *
    January 2020                                                            *
*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*
"""

import numpy as np
import sys
import time
import pickle
import pyglet

"""
Class Hexagon:
    Description:
        The hexagon is an object representing a cell in the snow crystal lattice.
    Parameters:
        u (float):
            Amount of water participating in diffusion
        v (float):
            Amount of water that does not participate in diffusion
        state (float):
            The water level in the cell
        mean_u (float):
            The mean u of the cell's neighbourhood
        receptive (boolean):
            If another cell in the cell's neighbourhood is ice
"""
class Hexagon:
    def __init__(self, u, v, state, mean_u, mean_s, receptive):
        self.u = u
        self.v = v
        self.state = state
        self.mean_u = mean_u
        self.mean_s = mean_s
        self.receptive = receptive

"""
Class CrystalLattice:
    Description:
        The crystal lattice is the main part of the simulation. It is a hexagonal
        grid using skew axial coordinates. Each coordinate contains a Hexagon
        object, the cells of the simulation. The simulation is run by continously
        calling the diffusion function.

    Parameters:
        lattice_size (int):
            Dimension of the lattice (View README for explanation)
        alpha (float):
            This is the diffusion coefficient
        beta (float):
            Background vapor level
        gamma (float):
            Vapor addition
        max_repetitions (int):
            Max number of iterations with no new frozen cells before program stops

    Functions:
        create_hexagonal_lattice:
            Description:
                Creates the hexagonal grid (the crystal lattice). The grid itself is
                a dictionary where the keys are skew axial coordinates for the hexagons
                and the values are Hexagon objects.

        frozen_area:
            Description:
                Calculates the current percentage of frozen cells

        get_neighbours:
            Description:
                Returns the coordinates of the neighbouring cells of a cell
            Parameters:
                hexagon_coordinates (tuple):
                    The coordinates of the cell in the center of the neighbourhood

        progress_tracking:
            Description:
                Updates count_down if the amount of frozen cells is the same as the
                previous time diffusion was called.

        umean_neighbours:
            Description:
                Returns the average amount of water that diffuses in a neighbourhood

        if_receptive:
            Description:
                Returns boolean on whether or not a cell is receptive for freezing.
                A cell is receptive if at least 1 neighbour is frozen.

        diffusion:
            Description:
                Performs diffusion simultaneously across the grid.
                Example for a cell:
                Calculates the the mean of u in the neighbourhood, checks if the cell
                is receptive, updates the values of u and v, updates the state.
"""
class CrystalLattice:
    def __init__(self, lattice_size, alpha, beta, gamma):
        self.size = lattice_size
        self.lattice = {}
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.max_repetitions = 20
        self.create_hexagonal_lattice()
        self.count_down = 0
        self.previous_frozen_area = 0
        self.diffusion_counter = 0
        self.sim_start_time = time.time()

    def create_hexagonal_lattice(self):
        # We're using an axial coordinate system.
        #   A lattice of size = 1
        #            ___
        #       ___/1,-1\____
        #     /0,-1\____/1, 0\
        #     \____/0, 0\____/
        #     /-1,0\____/0, 1\
        #     \____/-1,1\____/
        #          \____/

        for q in range(-self.size, self.size+1):
            for r in range(-self.size, self.size+1):
                # Making sure 'corners' are left out
                if (q + r) > self.size or (q + r) < -self.size:
                    continue
                # Flipping q and r sorts the lattice in this construction method
                if q != 0 or r != 0:
                    self.lattice[(r, q)] = Hexagon(self.beta, 0, self.beta, 0, 0, False)
                else:
                    self.lattice[(r, q)] = Hexagon(0, 1, 1, 0, 0, False)

    def frozen_area(self):
        return round(sum([1 for cell in self.lattice.keys() if self.lattice[cell].state >= 1]) / len(self.lattice) * 100, 2)

    def get_neighbours(self, hexagon_coordinates):
        # The neighbourhood of a hexagon
        #            ___
        #       ___/ 2  \____
        #     / 1  \____/ 3  \
        #     \____/    \____/
        #     / 6  \____/ 4  \
        #     \____/ 5  \____/
        #          \____/
        q, r = hexagon_coordinates[0], hexagon_coordinates[1] # On lattice
        neighbourhood = [(q, r-1), (q+1, r-1), (q+1, r),
                        (q, r+1), (q-1, r+1), (q-1, r)]
        # We make sure to check if the neighbour is within the lattice
        return [qr for qr in neighbourhood if qr in self.lattice]

    def progress_tracking(self):
        frozen = self.frozen_area()
        if frozen == self.previous_frozen_area:
            self.count_down += 1
            self.previous_frozen_area = frozen
        else:
            self.previous_frozen_area = frozen
            self.count_down = 0

    def umean_neighbours(self, coordinates):
        """
        returns the average amount of water that diffuses from the 6
        neighbours of a given cell
        """
        return np.mean([self.lattice[qr].u for qr in self.get_neighbours(coordinates)])

    def if_receptive(self, hexagon_coordinates):
        # if the cell itself is frozen
        if self.lattice[hexagon_coordinates].state >= 1:
            return True

        # if at least one of the cell's neighbours is frozen
        for hex in self.get_neighbours(hexagon_coordinates):
            if self.lattice[hex].state >= 1:
                return True

        # if neither the cell nor one of its neighbours is frozen
        return False

    def diffusion(self):
        self.diffusion_counter += 1
        for hex in self.lattice.keys():
            # calculate how much water diffuses from neighbour cells
            self.lattice[hex].mean_u = self.umean_neighbours(hex)

        # go through all cells and reset the u and v
        for hex in self.lattice.keys():
            # for receptive cells
            if self.if_receptive(hex):
                # no water diffuses
                self.lattice[hex].u = 0
                # all water stays in the cell
                self.lattice[hex].v = self.lattice[hex].state
                self.lattice[hex].receptive = True
            # for non-receptive cells
            else:
                # all water diffuses
                self.lattice[hex].u = self.lattice[hex].state
                # no water stays in the cell
                self.lattice[hex].v = 0

        for hex in self.lattice.keys():
            # implement the rules from reiter's model
            self.lattice[hex].u = self.lattice[hex].u + self.alpha/2 * (self.lattice[hex].mean_u - self.lattice[hex].u)

            # receptive cells
            if self.lattice[hex].receptive:
                self.lattice[hex].v = self.lattice[hex].v + self.gamma

            # for all cells state = u + v
            self.lattice[hex].state = self.lattice[hex].u + self.lattice[hex].v

        # keep track of simulation progress
        self.progress_tracking()
