import pygame
import os

# Centers window
x, y = 300, 70
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

# Game presets
fps = 60
width, height = 800, 600
grey = (37, 35, 35)
red = (255, 0 , 0)

#blah blah

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


while True:
    screen.fill(grey)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    pygame.display.update()
    clock.tick(fps)