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

"""
Reads saved pickles from experiments run from main.py and saved in the experiments
folder, then uses DrawCrystal to draw the crystal and save the image.
"""
if __name__ == '__main__':
    for filename in os.listdir('experiments/'):
        file = open(f'experiments/{filename}', 'rb')
        crystal = pickle.load(file)
        file.close()
        drawing = DrawCrystal(crystal, 500, hexagon_side_length=2, draw_program='PIL')
        drawing.draw()
