# from crystal_grid import *
import math
import pyglet

# hexgrid = create_hexagonal_grid(3)

def hexagon_corners(centerx, centery, size):
    degrees = [0, 60, 120, 180, 240, 300]
    rad = [math.pi / 180 * r for r in degrees]
    corners = [int(round(centerx)), int(round(centery))]
    for r in rad:
        corners.append(int(round(centerx + size * math.cos(r))))
        corners.append(int(round(centery + size * math.sin(r))))
    return tuple(corners)

c1 = hexagon_corners(300, 300, 50)
c2 = hexagon_corners(300, 300+(math.sqrt(3)*50), 50)
c3 = hexagon_corners(300, 300-(math.sqrt(3)*50), 50)
c4 = hexagon_corners(300+100*0.75, 300+(math.sqrt(3)*50)/2, 50)
c5 = hexagon_corners(300+100*0.75, 300-(math.sqrt(3)*50)/2, 50)
c6 = hexagon_corners(300-100*0.75, 300-(math.sqrt(3)*50)/2, 50)
c7 = hexagon_corners(300-100*0.75, 300+(math.sqrt(3)*50)/2, 50)

vertex_order = [0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 6, 0, 6, 1]

# iceblue = (220, 243, 255, 220, 243, 255, 220, 243, 255, 220, 243, 255, 220, 243, 255, 220, 243, 255, 220, 243, 255)
iceblue = (162,210,223,162,210,223,162,210,223,162,210,223,162,210,223,162,210,223,162,210,223)
print(c1)

hexagons = [c1, c2, c3, c4, c5, c6, c7]

class Window(pyglet.window.Window):
    def __init__(self):
        super(Window, self).__init__()
        self.set_size(600, 600)

    def on_draw(self):
        self.clear()
        # for hexagon in hexagons:
        #     pyglet.graphics.draw(6, pyglet.gl.GL_POINTS, ('v2i', hexagon))
        for hex in hexagons:
            pyglet.graphics.draw_indexed(7, pyglet.gl.GL_TRIANGLES,
                                        vertex_order, ('v2i', hex), ('c3B', iceblue))

if __name__ == '__main__':
    window = Window()
    pyglet.app.run()
