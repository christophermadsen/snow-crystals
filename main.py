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

class Window(pyglet.window.Window):
    def __init__(self, sim_type='animate', lattice_params=[70, 1, 0.3, 0.001]):
        super(Window, self).__init__(700, 700)
        # self.CL = CrystalLattice(70, alpha = 1, beta=0.3, gamma=0.0001)
        self.CL = CrystalLattice(*lattice_params)
        self.drawing = DrawCrystal(self.CL, self.get_size()[0], hexagon_side_length=2)
        self.sim_type = sim_type

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

if __name__ == '__main__':
    inp = input("Do you want to Animate, Draw or Experiment? (1/2/3): ")
    if inp == '1':
        window = Window()
        pyglet.app.run()
    elif inp == '2':
        window = Window(sim_type='draw')
        pyglet.app.run()
    elif inp == '3':
        pass
