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
from hexagonal_grid import CrystalLattice
import pyglet
import time
import csv

class Window(pyglet.window.Window):
    def __init__(self, beta, gamma):
        self.beta = beta
        self.gamma = gamma
        super(Window, self).__init__(600, 600)
        print(beta, gamma)
        self.CL = CrystalLattice(5, self.beta, self.gamma, alpha=1)
        self.drawing = DrawCrystal(self.CL, self.get_size()[0], hexagon_side_length=5)
        pyglet.clock.schedule_interval(self.update, 1.0/5)


    def on_draw(self):
        self.clear()
        self.drawing.draw()

    def update(self, dt):
        self.CL.diffusion()

testing = True
drawing = True


if __name__ == '__main__':
    if testing == True:
        # beta_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
        # gamma_values = [0, 0.0001, 0.001, 0.0035, 0.01, 0.05, 1]
        beta_values = [0.3, 0.5]
        gamma_values = [0.001, 0.0035]


        with open('statisticaloutcomes.csv','w') as fd:
            fd.write('beta,gamma,surface,time\n')

        for beta in beta_values:
            for gamma in gamma_values:
                window = Window(beta, gamma)
                pyglet.app.run()

    else:
        window = Window(beta=0.3, gamma=0.0001)
        pyglet.app.run()
