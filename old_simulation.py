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
import csv
start_time = time.time()

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
        self.create_hexagonal_lattice()

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
                    self.lattice[(r, q)] = Hexagon(self.beta, 0, self.beta, 0, 0, False, 0)
                else:
                    self.lattice[(r, q)] = Hexagon(0, 1, 1, 0, 0, False, 0)

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

    def all_ends_frozen(self):
        """
        Returns True if all 6 main branches are fully grown
        """
        frozen_ends = 0

        # coordinates of the ends of the main branches
        for coordinate in {(-(self.size-1), self.size-1), (self.size-1, -(self.size-1)),
        (0, self.size-1), (0, -(self.size-1)), (self.size-1, 0), (-(self.size-1), 0)}:

            # count the fully grown branches
            if self.lattice[coordinate].state >= 1:
                frozen_ends += 1

        frozen = 0
        for hex in self.lattice.keys():
            if self.lattice[hex].state >= 1:
                frozen += 1


        # if all branches are fully grown
        if frozen_ends == 6 or frozen_list[-1] == frozen_list[-2]:
            print('{}% frozen cells'.format(self.frozen_area()))
            print("--- %s seconds ---" % (time.time() - start_time))
            print('beta = {}, gamma = {}'.format(self.beta, self.gamma))
            pyglet.image.get_buffer_manager().get_color_buffer().save('images/beta={},gamma={}.png'.format(self.beta, self.gamma))
            pyglet.app.exit()
            return True

        else:
            return False

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

            # cells at the grid boundary stay the same
            if self.is_edge(hex):
                self.lattice[hex].u = self.beta

            else:
                # numerical approximation to the diffusion equation
                self.lattice[hex].u = self.lattice[hex].u + self.alpha/2 * (self.lattice[hex].mean_u - self.lattice[hex].u)

            # receptive, not edge cells
            if self.lattice[hex].receptive and not self.is_edge(hex):
                self.lattice[hex].v = self.lattice[hex].v + self.gamma

            # for all cells state = u + v
            self.lattice[hex].state = self.lattice[hex].u + self.lattice[hex].v

            # stop the simulation if all main branches are fully grown
        if self.all_ends_frozen():
            return True
