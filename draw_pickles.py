"""
.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.
Authors:                                                                    *
    Fenna Houtsma, Christopher Buch Madsen, Guido Vaessen                   *
                                                                            *
Date:                                                                       *
    January 2020                                                            *
*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*~.~*
"""

from drawing import DrawCrystal
import pickle
import os

if __name__ == '__main__':
    for filename in os.listdir('experiments/'):
        file = open(f'experiments/{filename}', 'rb')
        crystal = pickle.load(file)
        file.close()
        drawing = DrawCrystal(crystal, 700, hexagon_side_length=2, draw_program='PIL')
        drawing.draw()
