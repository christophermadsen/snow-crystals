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
<<<<<<< HEAD
    def __init__(self, sim_type='animate', lattice_params=[70, 1, 0.3, 0.001]):
        super(Window, self).__init__(700, 700)
        # self.CL = CrystalLattice(70, alpha = 1, beta=0.3, gamma=0.0001)
        self.CL = CrystalLattice(*lattice_params)
        self.drawing = DrawCrystal(self.CL, self.get_size()[0], hexagon_side_length=2)
        self.sim_type = sim_type
=======
    def __init__(self, beta, gamma):
        self.beta = beta
        self.gamma = gamma
        super(Window, self).__init__(600, 600)
        print(beta, gamma)
        self.CL = CrystalLattice(5, self.beta, self.gamma, alpha=1)
        self.drawing = DrawCrystal(self.CL, self.get_size()[0], hexagon_side_length=5)
        pyglet.clock.schedule_interval(self.update, 1.0/5)
>>>>>>> master

        if self.sim_type == 'animate':
            pyglet.clock.schedule_interval(self.update, 1.0/5)
        else:
            self.update(0.0001)

    def on_draw(self):
        self.clear()
        self.drawing.draw()

    def update(self, dt):
        if self.sim_type == 'animate':
            # draw for each timestep
            self.CL.diffusion()
        else:
            while True:
                # stop the program if the main branches are fully grown
                if self.CL.diffusion():
                    break

testing = True
drawing = True


if __name__ == '__main__':
<<<<<<< HEAD
    inp = input("Do you want to Animate, Draw or Experiment? (1/2/3): ")
    if inp == '1':
        window = Window()
        pyglet.app.run()
    elif inp == '2':
        window = Window(sim_type='draw')
        pyglet.app.run()
    elif inp == '3':
        pass
=======
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
>>>>>>> master
