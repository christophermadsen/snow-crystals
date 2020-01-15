"""
.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.
Authors:                                                                    *
    Fenna Houtsma, Christopher Buch Madsen, Guido Vaessen                   *
                                                                            *
Date:                                                                       *
    January 2020                                                            *
*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*
"""
class Hexagon:
    def __init__(self, u, v, state):
        self.u = u
        self.v = v
        self.state = state

class CrystalLattice:
    def __init__(self, lattice_size, alpha=0.5, beta=0.5, gamma=0.5):
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
                if q == 0 and r == 0:
                    self.lattice[(r, q)] = Hexagon(0, 0, 1)
                else:
                    self.lattice[(r, q)] = Hexagon(0, 0, self.beta)

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

    def umean_neighbours(self, hexagon_coordinates):
        neighbours_u = [self.lattice[qr].u for qr in self.get_neighbours(hexagon_coordinates)]
        return sum(neighbours_u)/len(neighbours_u)

    def if_receptive(self, hexagon_coordinates):
        neighbours = self.get_neighbours(hexagon_coordinates)
        for hex in neighbours:
            state = self.lattice[hex].state
            if state == 1:
                return True
        return False

    def diffusion(self):
        for coordinate in self.lattice.keys():
            if self.if_receptive(coordinate):
                self.lattice[coordinate].u = 0
                self.lattice[coordinate].v = self.lattice[coordinate].state
            else:
                self.lattice[coordinate].u = self.lattice[coordinate].state
                self.lattice[coordinate].v = 0

        for hexagon, coordinate in zip(self.lattice.values(), self.lattice.keys()):
            self.lattice[coordinate].u = hexagon.u + self.alpha/2 * (self.umean_neighbours(coordinate) - hexagon.u)
            self.lattice[coordinate].v = hexagon.v + self.gamma
            self.lattice[coordinate].state = hexagon.u + hexagon.v
