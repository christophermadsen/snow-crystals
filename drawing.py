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
import PIL.ImageDraw as ImageDraw, PIL.Image as Image

"""
Class DrawCrystal:
    Description:
        Uses a CrystalLattice object to calculate the pixel coordinates for each
        cell in a window. Then uses either pyglet or PIL to create a drawing from
        the current states of the cells and their coordinates.
    Parameters:
        CrystalLatticeObject (object):
            A CrystalLattice object
        window_size (int):
            The quadratic size for the window to display the drawin in
        hexagon_side_length (int):
            The pixel length of the sides of a hexagon
        draw_program (str):
            'pyglet' and 'PIL' may be used to choose a drawing program.
            PIL is used for the experimental part in main.py and pyglet is used
            for the animate and draw options.

    Functions:
        hexagon_corners:
            Description:
                Calculates the pixel coordinates of the vertices of a hexagon
            Parameters:
                x, y (int):
                    Coordinates of the center vertex in a hexagon
        compute_offsets:
            Description:
                Computes the placement of a hexagon in the window based on it's
                skew axial coordinate in the CrystalLattice object.
            Parameters:
                hexagon_coordinates:
                    Coordinates of a cell in the CrystalLattice object
        calculate_lattice_drawing_coordinates:
            Utilizes the other functions to calculate all vertex coordinates in
            the drawing window.
        draw:
            uses either the pyglet or PIL package to draw the hexagons with
            pixel coordinates calculated by calculate_lattice_drawing_coordinates
            and fills in a color based on the state of each cell.
"""
class DrawCrystal:
    def __init__(self, CrystalLatticeObject, window_size, hexagon_side_length, draw_program='pyglet'):
        self.CL = CrystalLatticeObject
        self.window_size = window_size
        self.centerx, self.centery = [int(round((window_size/2) - 1))] * 2
        self.hex_size = hexagon_side_length
        self.vertex_order = [0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 6, 0, 6, 1]
        self.iceblue = tuple([162, 210, 223] * 7)
        self.ice_white = tuple([255, 255, 255] * 7)
        self.degrees = [0, 60, 120, 180, 240, 300]
        self.radians = [math.pi / 180 * r for r in self.degrees]
        self.style = draw_program
        self.calculate_lattice_drawing_coordinates()

    def hexagon_corners(self, x, y):
        if self.style == 'pyglet':
            corners = [int(round(x)), int(round(y))]
            for r in self.radians:
                corners.append(int(round(x + self.hex_size * math.cos(r))))
                corners.append(int(round(y + self.hex_size * math.sin(r))))
            return tuple(corners)

        elif self.style == 'PIL':
            corners = []
            for r in self.radians:
                c1 = int(round(x + self.hex_size * math.cos(r)))
                c2 = int(round(y + self.hex_size * math.sin(r)))
                corners.append((c1, c2))
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
        if self.style == 'pyglet':
            for hexagon, hex_object in zip(self.drawing_coordinates, self.CL.lattice.values()):
                if hex_object.state >= 1:
                    pyglet.graphics.draw_indexed(7, pyglet.gl.GL_TRIANGLES,
                                            self.vertex_order, ('v2i', hexagon),
                                            ('c3B', self.ice_white))

                else:
                    color = int(255 * hex_object.state)
                    color = tuple([color, color, color] * 7)
                    pyglet.graphics.draw_indexed(7, pyglet.gl.GL_TRIANGLES,
                                            self.vertex_order, ('v2i', hexagon),
                                            ('c3B', color))

        elif self.style == 'PIL':
            image = Image.new("RGB", (self.window_size, self.window_size))
            draw = ImageDraw.Draw(image)
            self.calculate_lattice_drawing_coordinates()

            for hexagon, hex_object in zip(self.drawing_coordinates, self.CL.lattice.values()):
                if hex_object.state >= 1:
                    draw.polygon(hexagon, fill=(255, 255, 255))
                else:
                    color = int(255 * hex_object.state)
                    color = tuple([color] * 3)
                    draw.polygon(hexagon, fill=color)
            image.save(f"images/beta={self.CL.beta},gamma={self.CL.gamma}.png")
