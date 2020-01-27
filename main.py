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
from simulation import CrystalLattice
import pyglet
import time
import csv

class Window(pyglet.window.Window):
    def __init__(self, lattice):
        super(Window, self).__init__(500, 500)
        self.CL = lattice
        self.drawing = DrawCrystal(self.CL, self.get_size()[0], hexagon_side_length=2)
        self.start_time = time.time()
        pyglet.clock.schedule_interval(self.update, 1.0/60)

    def on_draw(self):
        self.clear()
        self.drawing.draw()

    def update(self, dt):
        if self.CL.count_down == 20:
            print(f"Frozen cells: {self.CL.frozen_area()}%")
            print(f"--- {time.time() - self.start_time} seconds")
            print(f"beta={self.CL.beta}, gamma={self.CL.gamma}")
            pyglet.image.get_buffer_manager().get_color_buffer().save(f"images/beta=crap, gamma={self.CL.gamma}.png")
            pyglet.app.exit()
        else:
            self.CL.diffusion()

if __name__ == '__main__':
    # The lattice for the 'animate' and 'draw' options
    lattice_params = [70, 1, 0.3, 0.001] #grid dim, alpha, beta, gamma
    lattice = CrystalLattice(*lattice_params)

    inp = input("Do you want to animate, draw or experiment? ")
    if inp == 'animate' or inp == '1':
        sim = Window(lattice)
        pyglet.app.run()
    elif inp == 'draw' or inp == '2':
        t = time.time()
        while lattice.count_down < 20:
            lattice.diffusion()
            print(f"time elapsed: {time.time() - t:.2f} seconds", end="\r")
        print(f"Frozen cells: {lattice.frozen_area()}%")
        print(f"--- {time.time() - lattice.sim_start_time} seconds")
        print(f"beta={lattice.beta}, gamma={lattice.gamma}")
        sim = Window(lattice)
        pyglet.app.run()
        pyglet.app.exit()
    elif inp == 'experiment' or inp =='3':
        pass
