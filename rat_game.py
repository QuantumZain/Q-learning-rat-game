import pygame
from random import randint
import os

# Centers window
x, y = 300, 70
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

# Game presets
fps = 60
width, height = 800, 600
grey = (37, 35, 35)
red = (255, 0 , 0)
white = (240, 240, 240)
gold = (250, 210, 20)
orange = (240, 150, 20)

# generate a 6x6 grid
cell_width = 60
D = 6 # dimensions
thickness = 3

class Entity:
    score = 0 # player's score
    identities = ["player", "bomb", "home"]
    entities = []

    def __init__(self, index, identitiy):
        self.index = index
        self.identitiy = identitiy
        Entity.entities.append(self)
    
    def restart():
        '''Restarts game after squirel dies or wins, but doesn't reset score'''
        # Entity.entities = []
        # initialize_players()
        for entity in Entity.entities:
            iden = entity.identitiy
            if iden == "player":
                entity.index = 3
            if iden == "bomb":
                entity.index = randint(1, D**2 -2)
        print(f"current score: {Entity.score}")


    def up(self):
        if self.index - 6 >= 0:
            self.index -= 6
            Entity.score -= 1
    def down(self):
        if self.index + 6 <= 35:
            self.index += 6
            Entity.score -= 1
    def right(self):
        if self.index + 1 <= 35:
            self.index += 1
            Entity.score -= 1
    def left(self):
        if self.index - 1 >= 0:
            self.index -= 1
            Entity.score -=1



    def state_handler(self, mob):
        if self.index == mob.index and self.identitiy == "player" and mob.identitiy == "bomb":
            print("you died")
            Entity.score -= 100
            Entity.restart()
        
        if self.index == mob.index and self.identitiy == "player" and mob.identitiy == "home":
            print("you win")
            Entity.score += 100
            Entity.restart()
        



def draw_square(side_length, posx, posy, color, thickness):
    square = pygame.Rect(posx, posy, side_length, side_length)
    pygame.draw.rect(screen, color, square, thickness)


def draw_grid(cell_width, dimensions, color, thickness) -> list:
    ''' a centered nxn grid with n = dimensions, locx and locy is the location of top left corner
    returns the cell_matrix '''
    grid_length = (cell_width + thickness)*dimensions

    locx, locy = (width - grid_length)//2, (height-grid_length)//2
    # print(locx, locy)
    posx, posy = locx, locy
    for n in range(dimensions):
        for m in range(dimensions):
            draw_square(cell_width, posx + m*cell_width, posy+n*cell_width, color, thickness)
    return [(locx + cell_width*x, locy + cell_width*(x%dimensions)) for x in range(6*6)]


def draw_circle(rad, col, center):
    pygame.draw.circle(screen, col, center, rad)


def get_cell_matrix():

    grid_length = (cell_width + thickness)*D
    locx, locy = (width - grid_length)//2, (height-grid_length)//2

    return [(locx + cell_width*(x%D + 0.5)//1, locy + cell_width*(x//D +0.5)//1) for x in range(6*6)]

def make_bombs(num):
    locations = [randint(1, D**2 -2) for i in range(num)]
    for location in locations:
        # rindex = randint(1, D**2 -1)
        Entity(location, Entity.identities[1])


def initialize_players():
    squirrel = Entity(3, Entity.identities[0])
    home = Entity(35, Entity.identities[2])
    make_bombs(4)

cell_matrix = get_cell_matrix()
initialize_players()

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


while True:
    screen.fill(grey)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            for entity in Entity.entities:
                if entity.identitiy == "player":
                    squirrel = entity
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        squirrel.up()
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        squirrel.down()
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        squirrel.left()
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        squirrel.right()
            
    draw_grid(cell_width, D, white, 3)
    
    for entity in Entity.entities:
        squirrel = Entity.entities[0]
        color_table = {"player": gold, "bomb": red, "home": orange}
        color = color_table[entity.identitiy]
        draw_circle(cell_width//3, color, cell_matrix[entity.index])
        squirrel.state_handler(entity)

    
    
    pygame.display.update()
    clock.tick(fps)
