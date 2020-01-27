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
import pandas as pd
import pyglet
import time
import pickle

class Window(pyglet.window.Window):
    def __init__(self, lattice):
        super(Window, self).__init__(500, 500)
        self.CL = lattice
        self.drawing = DrawCrystal(self.CL, self.get_size()[0], hexagon_side_length=2)
        self.start_time = time.time()
        self.safety_counter = 0
        pyglet.clock.schedule_interval(self.update, 1.0/24)
        # self.drawing.draw()

    def on_draw(self):
        self.clear()
        self.drawing.draw()

    def update(self, dt):
        if self.CL.count_down > 19 and self.safety_counter < 1:
            self.safety_counter += 1
        elif self.CL.count_down > 19 and self.safety_counter > 0:
            print(f"Frozen cells: {self.CL.frozen_area()}%")
            print(f"--- {time.time() - self.start_time} seconds")
            print(f"beta={self.CL.beta}, gamma={self.CL.gamma}")
            pyglet.image.get_buffer_manager().get_color_buffer().save(f"images/beta={self.CL.beta}, gamma={self.CL.gamma}.png")
            self.close()
        else:
            self.CL.diffusion()

if __name__ == '__main__':
    # The lattice for the 'animate' and 'draw' options
    lattice_params = [70, 1, 0, 0] #grid dim, alpha, beta, gamma
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
        # pyglet.app.exit()

    elif inp == 'experiment' or inp =='3':
        beta_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
        gamma_list = [0, 0.0001, 0.001, 0.0035, 0.01, 0.05, 1]
        beta_list = [0, 0.1]
        gamma_list = [0]
        n_exp = len(beta_list) * len(gamma_list)

        t = time.time()
        exp = 1
        outcomes = []
        for gamma in gamma_list:
            for beta in beta_list:
                lattice = CrystalLattice(70, 1, beta, gamma)
                while lattice.count_down < 20:
                    lattice.diffusion()
                    print(f"Experiment: {exp}/{n_exp}, time elapsed: {time.time() - t:.2f}", end="\r")
                exp += 1
                outcomes.append([lattice.diffusion_counter, lattice.frozen_area(), lattice.beta, lattice.gamma])
                file = open(f"experiments/beta={beta}_gamma={gamma}.pickle", 'wb')
                pickle.dump(lattice, file)
                file.close()
        pd.DataFrame(outcomes, columns=['diffusion_count', 'frozen_area', 'beta', 'gamma']).to_csv('statisticaloutcomes.csv', index=False)
