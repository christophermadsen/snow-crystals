"""
.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.
Authors:                                                                    *
    Fenna Houtsma, Christopher Buch Madsen, Guido Vaessen                   *
                                                                            *
Date:                                                                       *
    January 2020                                                            *
                                                                            *
Project description:                                                        *
    Simulating snow crystals and researching the underlying conditions for  *
    which the 6 archetypes depend in their formation.                       *
*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*
"""

def create_hexagonal_grid(boundary=3):
    # We're using an axial coordinate system.
    #   A hexagon with boundary=1
    #            ___
    #       ___/1,-1\____
    #     /0,-1\____/1, 0\
    #     \____/0, 0\____/
    #     /-1,1\____/0, 1\
    #     \____/-1,1\____/
    #          \____/
    coordinates = {}
    for q in range(-boundary, boundary+1):
        for r in range(-boundary, boundary+1):
            # Making sure 'corners' are left out
            if (q + r) > boundary or (q + r) < -boundary:
                continue
            # Flipping q and r sorts the grid in this construction method
            coordinates[(r, q)] = 0
    return coordinates

def get_neighbours(grid, hexagon):
    # The neighbourhood of a hexagon
    #            ___
    #       ___/ 2  \____
    #     / 1  \____/ 3  \
    #     \____/    \____/
    #     / 6  \____/ 4  \
    #     \____/ 5  \____/
    #          \____/
    q, r = hexagon[0], hexagon[1]
    neighbourhood = [(q, r-1), (q+1, r-1), (q+1, r), (q, r+1), (q-1, r+1), (q-1, r)]
    # We make sure to check if the neighbour is on the grid
    return [qr for qr in neighbourhood if qr in grid]

# hexgrid = create_hexagonal_grid(3)
