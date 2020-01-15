"""
.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.
Authors:                                                                    *
    Fenna Houtsma, Christopher Buch Madsen, Guido Vaessen                   *
                                                                            *
Date:                                                                       *
    January 2020                                                            *
*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*
"""

from hexagonal_grid import CrystalLattice
import math
import pyglet

def hexagon_corners(centerx, centery, size):
    degrees = [0, 60, 120, 180, 240, 300]
    rad = [math.pi / 180 * r for r in degrees]
    corners = [int(round(centerx)), int(round(centery))]
    for r in rad:
        corners.append(int(round(centerx + size * math.cos(r))))
        corners.append(int(round(centery + size * math.sin(r))))
    return tuple(corners)

def compute_offsets(centerx, centery, size, hexagon_coordinates):
    q, r = hexagon_coordinates
    w = size * 2 # Width of a hexagon
    h = math.sqrt(3) * size # Height of a hexagon
    hoffset = w * 0.75 # Horizontal offset to next hexagon center
    new_x = centerx + q * hoffset # x is independent from q
    new_y = centery + (r * h) + (q * h)/2 # when moving q, h/2 is added to y
    return new_x, new_y

hexgrid = CrystalLattice(30)

size = 5
hexagons = []
for key in hexgrid.lattice:
    x, y = compute_offsets(300, 300, size, key)
    hexagons.append(hexagon_corners(x, y, size))

vertex_order = [0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 6, 0, 6, 1]
iceblue = (162,210,223,162,210,223,162,210,223,162,210,223,162,210,223,162,210,223,162,210,223)

class Window(pyglet.window.Window):
    def __init__(self):
        super(Window, self).__init__()
        self.set_size(600, 600)

    def on_draw(self):
        self.clear()
        for hex in hexagons:
            pyglet.graphics.draw_indexed(7, pyglet.gl.GL_TRIANGLES,
                                        vertex_order, ('v2i', hex), ('c3B', iceblue))

if __name__ == '__main__':
    window = Window()
    pyglet.app.run()

# grid = {(3, 3) : cell1,
#         (0, 0) : cell25,
#         ... }
#
# 1. Make grid/cell classes
# 2. Draw hexagons in a smart way
# 3. Make sure timestep loop works
# 4. Implement rules

# class Grid:
#     def __init__(self, dimensions, initialization_parameters...):
#         self.dim = dimensions
#         params...
#
#     def make_grid(self):
#         grid code...
#
#     def get_neighbours(self, hexagon):
#         hexagon code...
#
#     def diffusion(self):
#         for every hexagon coordinate:
#             get_neighbours(coordinates)
#             calculate diffusion
#             update Cell at coordinate
#
#     class Cell:
#         def __init__(self, u, v):
#             self.u = u
#             self.v = v
#             ...
#
#
# grid = Grid(3, parameters)
# update loop (1000):
#     grid.diffuse()
#     grid.some_other_methods()
#     ...
#     grid draw
