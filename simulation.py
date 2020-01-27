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

class Hexagon:
    def __init__(self, u, v, state, mean_u, mean_s, receptive):
        self.u = u
        self.v = v
        self.state = state
        self.mean_u = mean_u
        self.mean_s = mean_s
        self.receptive = receptive

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
        self.sim_start_time = time.time()

    def create_hexagonal_lattice(self):
        # We're using an axial coordinate system.
        #   A lattice of size = 1
        #            ___
        #       ___/1,-1\____
        #     /0,-1\____/1, 0\
        #     \____/0, 0\____/
        #     /-1,1\____/0, 1\
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
        # returns the percentage of frozen area
        return round(sum([1 for cell in self.lattice.keys() if self.lattice[cell].state >= 1]) / len(self.lattice) * 100, 2)

    def eq_neighbours(self, coordinates):
        r = coordinates[0]
        q = coordinates[1]
        if r < 0 and r%2 == 0 and q > 0:
            return (r+1, q-1), (r+1, q-2)
        elif r > 0 and r%2 == 0 and q < 0:
            return (r-1, q-1), (r-1, q+2)
        elif r > 0 and q < 0 and q%2 == 0:
            return (r+1, q+1), (r-2, q+1)
        elif r < 0 and q > 0 and q%2 == 0:
            return (r+2, q-1), (r-1, q-1)
        elif (r < 0 and q > 0) or (r > 0 and q < 0):
            return (r-1, q-1), (r+1, q+1)
        elif r != 0:
            return (r+1, q-2), (r-1, q+2)
        elif q > 0:
            return (r-2, q+1), (r+2, q-1)
        elif r == 0:
            return (r+2, q-1), (r-2, q+1)
        elif q == 0:
            return (r-1, q+2), (r+1, q-2)

    def smean_eq_neighbours(self, cell):
        return (1/3) * (self.lattice[cell].state + self.lattice[self.eq_neighbours(cell)[0]].state
        + self.lattice[self.eq_neighbours(cell)[1]].state)

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

    def is_edge(self, coordinates):
        """
        edge cells are defined at the cells at the boundaries of the grid
        for these cells either q or r should be equal to +- the grid dimensions
        """
        if coordinates[0] in [self.size, -self.size] or coordinates[1] in [self.size, -self.size]:
            return True
        else:
            return False

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
        """
        A cell is receptive if it or at least one of its neighbours is frozen,
        this functions returns a boolean on whether or not a cell is receptive
        """
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
        for hex in self.lattice.keys():
            # calculate how much water diffuses from neighbour cells
            self.lattice[hex].mean_u = self.umean_neighbours(hex)

            # self.lattice[hex].mean_s = self.smean_eq_neighbours(hex)

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
            if self.lattice[hex].receptive and not self.is_edge(hex):
                self.lattice[hex].v = self.lattice[hex].v + self.gamma

            # for all cells state = u + v
            self.lattice[hex].state = self.lattice[hex].u + self.lattice[hex].v

        # keep track of simulation progress
        self.progress_tracking()

"""
The following part is from the enhanced reiter's model section of the
Li paper, but it doesn't work properly yet because the wrong eq_neighbours
are returned from the eq_neighbours function
"""
            # if both neighbours of the current cell aren't frozen
            # neighbour0 = self.lattice[self.eq_neighbours(hex)[0]]
            # neighbour1 = self.lattice[self.eq_neighbours(hex)[1]]

            # if both neighbours of the current cell aren't frozen
            # if all(state < 1 for state in (neighbour1.state, neighbour2.state)):
            #
            #     self.lattice[hex].delta +=  self.epsilon * (self.lattice[hex].mean_s - self.lattice[hex].state)
            #
            #     self.lattice[self.eq_neighbours(hex)[0]].delta += self.epsilon * (self.lattice[hex].mean_s - neighbour0.state)
            #
            #     self.lattice[self.eq_neighbours(hex)[1]].delta += self.epsilon * (self.lattice[hex].mean_s - neighbour1.state)
            #
            # self.lattice[hex].state += self.lattice[hex].delta
