import pyglet
from snowflake import Snowflake_Model

""" Making the cellular automata grid:
The grid is made using pyglet package, where you can create
a window. """

class Window(pyglet.window.Window):

    def __init__(self):
        super(Window, self).__init__(600, 600)
        self.snowflakemodel = Snowflake_Model(self.get_size()[0],
                                            self.get_size()[1],
                                            20, 0, 0, 0)
        pyglet.clock.schedule_interval(self.update, 1.0)

    def on_draw(self):
        self.clear()
        self.snowflakemodel.draw()

    def update(self, dt):
        self.snowflakemodel.run_rules()


if __name__ == '__main__':
    window = Window()
    pyglet.app.run()
