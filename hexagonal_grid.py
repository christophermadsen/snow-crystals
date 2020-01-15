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
    def __init__(self, u=1, v=1):
        self.u = u
        self.v = v
        # ...

class CrystalLattice:
    def __init__(self, lattice_size):
        self.size = lattice_size
        self.lattice = {}
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
                self.lattice[(r, q)] = Hexagon()

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

    def diffusion(self):
        pass
        # for every hexagon coordinate:
        #     get_neighbours(coordinates)
        #     calculate diffusion
        #     update Cell at coordinate

    def whatever(self):
        pass
        # ...
