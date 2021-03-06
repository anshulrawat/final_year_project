import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg


import pygame
from pygame.locals import *
import pylab

def animate(screen):
    fig = pylab.figure(figsize=[2, 2], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
    ax = fig.gca()
    for i in range(100):
        y1=(1+i)%4
        y2=(2+i)%4
        y3 = (3 + i) % 4
        ax.plot([y1, y2, y3])

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (0, 0))



pygame.init()

window = pygame.display.set_mode((600, 400), DOUBLEBUF)
screen = pygame.display.get_surface()
animate(screen)
pygame.display.flip()

crashed = False
while not crashed:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			crashed = True