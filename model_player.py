from Environment import Entity
import pygame
import os
import random
import time as t
import numpy as np
import matplotlib.pyplot as plt

# Centers window
x, y = 300, 70
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

# Game window presets
FPS = 6
WIDTH, HEIGHT = 800, 600
grey = (37, 35, 35)
red = (255, 0 , 0)
white = (240, 240, 240)
gold = (250, 210, 20)
orange = (240, 150, 20)

# players and render presets
CELL_WIDTH = 60
DIM = Entity.DIM # dimensions
THICKNESS = 3
Entity.INIT_VARS = (2, DIM**2-1, 4)

# Bellman equation constants
DISCOUNT = 0.95
LEARNING_RATE = 0.1
MAX_STEPS = 20
EPISODES = 450_000


# initialize environment and players
Entity.initialize_players()
Entity.init_class(MAX_STEPS) # sets max steps before simulation terminates.
player = Entity.entities[0]

action_dic = {
    0: "up",
    1: "right",
    2: "down",
    3: "left",
}

def draw_square(screen, side_length, posx, posy, color, thickness):
    square = pygame.Rect(posx, posy, side_length, side_length)
    pygame.draw.rect(screen, color, square, thickness)


def draw_grid(screen, cell_width, dimensions, color, thickness) -> list:
    ''' a centered nxn grid where n is dimensions, locx and locy are the location of top left corner
    and function returns the cell_matrix '''
    grid_length = (cell_width + thickness)*dimensions

    locx, locy = (WIDTH - grid_length)//2, (HEIGHT-grid_length)//2
    # print(locx, locy)
    posx, posy = locx, locy
    for n in range(dimensions):
        for m in range(dimensions):
            draw_square(screen, cell_width, posx + m*cell_width, posy+n*cell_width, color, thickness)
    # return [(locx + cell_width*x, locy + cell_width*(x%dimensions)) for x in range(6*6)]


def get_cell_matrix():
    '''returns the coordinates of the centers of each cell of the grid'''
    grid_length = (CELL_WIDTH + THICKNESS)*DIM
    locx, locy = (WIDTH - grid_length)//2, (HEIGHT-grid_length)//2

    return [(locx + CELL_WIDTH*(x%DIM + 0.5)//1, locy + CELL_WIDTH*(x//DIM +0.5)//1) for x in range(DIM*DIM)]


def show_render(render: bool):
    if render:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        screen.fill(grey)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        draw_grid(screen, CELL_WIDTH, DIM, white, 3)
        
        for entity in Entity.entities:
            cell_matrix = get_cell_matrix()
            color_table = {"player": gold, "bomb": red, "home": orange} #! set dynamically later
            color = color_table[entity.identitiy]

            pygame.draw.circle(screen, color, cell_matrix[entity.index], CELL_WIDTH//3)
        pygame.display.flip()
        clock.tick(FPS)
    else:
        pygame.quit()


# dim**2 is the number of possible possitions, 2 is whether or not theres a bomb in a particular direction
state_space = (DIM**2, 2, 2, 2)
action_space = (4,)

# q_table = np.random.uniform(low= -20, high= 10, size=(state_space + action_space))
# OR load previously trained q_table
q_table = np.load("models/q_table_98000.npy")

wins = 0
win_record = []
init_state = player.get_state()

ep_score = []
action_book = {}
state_book = {}
rewards_statistic = {"ep": [], "avg": [], "min": [], "max": []}


for episode in range(EPISODES):

    is_over = False
    state = init_state
    Entity.restart()
    # print(f"epsilon: {epsilon}")
    wins_every = 0

    action_list = []
    state_list = [player.get_state()]
    while not is_over:
        show_render(True)
        
        # APPLYING BELLMAN'S equation
        action = np.argmax(q_table[state]) # gets the index of the largest q val
        action_list.append(action)

        *new_state, reward, is_over = player.env_step(action)
        new_state = new_state[0]
        state_list.append(new_state)
        

        max_future_q = np.max(q_table[new_state])
        current_q = q_table[state + (action, )]
        
        if reward > 10:
            print(f"#{episode} I WON DAD! at") #{state[0]}")
            wins += 1
            wins_every += 1

        # update old state to new state
        state = new_state
        ###########################
        
        # print(f"Episode {episode} - score: {Entity.score} at step: {Entity.playerSteps}")
        # print("---------")
        # print(f"#{episode} - score {Entity.score}")

print(f"THE END\n------------\nWe have won {wins} times out of {EPISODES} episodes or {len(ep_score)}")


