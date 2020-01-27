"""
.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.
Authors:                                                                    *
    Fenna Houtsma, Christopher Buch Madsen, Guido Vaessen                   *
                                                                            *
Date:                                                                       *
    January 2020                                                            *
*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*
"""

from simulation import CrystalLattice, Hexagon
import math
import pyglet

class DrawCrystal:
    def __init__(self, CrystalLatticeObject, window_size, hexagon_side_length):
        self.CL = CrystalLatticeObject
        self.centerx, self.centery = [int(round((window_size/2) - 1))] * 2
        self.hex_size = hexagon_side_length
        self.vertex_order = [0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 6, 0, 6, 1]
        self.iceblue = tuple([162, 210, 223] * 7)
        self.ice_white = tuple([255, 255, 255] * 7)
        self.grey = tuple([])
        self.degrees = [0, 60, 120, 180, 240, 300]
        self.radians = [math.pi / 180 * r for r in self.degrees]
        self.calculate_lattice_drawing_coordinates()






    def hexagon_corners(self, x, y):
        corners = [int(round(x)), int(round(y))]
        for r in self.radians:
            corners.append(int(round(x + self.hex_size * math.cos(r))))
            corners.append(int(round(y + self.hex_size * math.sin(r))))
        return tuple(corners)

    def compute_offsets(self, hexagon_coordinates):
        q, r = hexagon_coordinates
        w = self.hex_size * 2 # Width of a hexagon
        h = math.sqrt(3) * self.hex_size # Height of a hexagon
        hoffset = w * 0.75 # Horizontal offset to next hexagon center
        new_x = self.centerx + q * hoffset # x is independent from q
        new_y = self.centery + (r * h) + (q * h)/2 # when moving q, h/2 is added to y
        return new_x, new_y

    def calculate_lattice_drawing_coordinates(self):
        self.drawing_coordinates = []
        for hexagon in self.CL.lattice:
            x, y = self.compute_offsets(hexagon)
            self.drawing_coordinates.append(self.hexagon_corners(x, y))

    def draw(self):
        for hexagon, hex_object in zip(self.drawing_coordinates, self.CL.lattice.values()):
            if hex_object.state >= 1:
                pyglet.graphics.draw_indexed(7, pyglet.gl.GL_TRIANGLES,
                                        self.vertex_order, ('v2i', hexagon),
                                        ('c3B', self.ice_white))
            elif 0 < hex_object.state < 1:
                color = int(255 * hex_object.state)
                color = tuple([color, color, color] * 7)
                pyglet.graphics.draw_indexed(7, pyglet.gl.GL_TRIANGLES,
                                        self.vertex_order, ('v2i', hexagon),
                                        ('c3B', color))
