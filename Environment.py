from random import randint, choice
import os
import pygame
# # generate a 6x6 grid
# cell_width = 60
# thickness = 3
# init_vars = (3, 35, 4) # player initial ind, home's index, numbe of bombs/obstacles

class Entity():
    DIM = 6 # dimensions
    score = 0 # player's score
    identities = ["player", "bomb", "home"]
    entities = []
    INIT_VARS = (2, 35, 7)
    playerSteps = 0
    STEPS_THRESH = int()
    reward = 0

    # consider tweaking punishment
    reward_rubric = {
        "bomb": int(),
        "home": int(),
        "otherwise": -3, # if identity is "player" this will assign none to reward but will be overriden quickly
    }

    @classmethod
    def init_class(cls, steps_thresh):
        bias = 2
        cls.STEPS_THRESH = steps_thresh
        cls.reward_rubric["bomb"] = steps_thresh*Entity.reward_rubric["otherwise"] - bias
        cls.reward_rubric["home"] = abs(cls.reward_rubric["bomb"])
    
    
    def __init__(self, index, identitiy):
        self.index = index
        self.identitiy = identitiy
        self.rewards_tracker = []
        Entity.entities.append(self)


    # Looks like shit please simplify
    def up(self):
        if self.index - Entity.DIM >= 0:
            self.index -= Entity.DIM
        # Entity.reward = -3
        # Entity.score += Entity.reward
    def down(self):
        if self.index + Entity.DIM <= Entity.DIM**2 -1: 
            self.index += Entity.DIM
        # Entity.reward = -3
        # Entity.score += Entity.reward
    def right(self):
        if self.index + 1 <= Entity.DIM**2 - 1:
            self.index += 1
        # Entity.reward = -3
        # Entity.score += Entity.reward
    def left(self):
        if self.index - 1 >= 0:
            self.index -= 1
        # Entity.reward = -3
        # Entity.score += Entity.reward
    def do_action(self, action):
        
        action_dic = {
        0: self.up,
        1: self.right,
        2: self.down,
        3: self.left
        }
        action_dic[action]()

     
    # def restart(player_ind=init_vars[0]):
    @classmethod
    def restart(cls):
        '''Restarts game after squirel dies or wins and resets player.index back to the starting index player_ind '''
        player_ind = cls.INIT_VARS[0]
        bombs_indicies = []
        for entity in Entity.entities:
            iden = entity.identitiy
            if iden == "player":
                entity.index = player_ind
            elif iden == "bomb":
                allset = {i+1 for i in range(Entity.DIM**2-1)}
                forbid_set = {player_ind, Entity.entities[1].index}
                allowed = list(allset.difference(forbid_set))
                if len(bombs_indicies) > 1:
                    home_ind = cls.INIT_VARS[1]
                    for ind in (player_ind-1, player_ind+1, player_ind+Entity.DIM,
                               home_ind-1, home_ind-Entity.DIM):
                        if ind in bombs_indicies:
                            allowed.remove(ind)
                entity.index = choice(allowed) # reset existing bombs' locations
                bombs_indicies.append(entity.index)
                # randos = [i+1 for i in range(Entity.DIM**2 - 2) if (i+1 != player_ind)]
        
        # print(f"Run's final score: {Entity.score}")
        cls.score = 0
        # print(f"score reset to {Entity.score}")


    # # def state_handler(self, mob, player_ind):
    def state_handler(self):
        is_over = False
        for entity in Entity.entities:
            mob = entity
            if mob.identitiy == "player":
                continue
            if self.index == mob.index:
                if mob.identitiy == "bomb":
                    print(f"sorry dad")
                Entity.reward = Entity.reward_rubric[mob.identitiy]
                # print(f"with reward: {Entity.reward}")
                # if Entity.playerSteps == 1:
                #     print(f"{Entity.reward} - <reward: state_handler()>")
                Entity.score += Entity.reward
                # print(f"{Entity.score} - <Entity.py: state_handler()>")
                is_over = True
                Entity.playerSteps = 0 # reset steps count
            if Entity.playerSteps >= Entity.STEPS_THRESH:
                Entity.score += Entity.reward
                # print(f"{Entity.score} - <Entity.py: state_handler()>")
                is_over = True
                Entity.playerSteps = 0 # reset steps count
        if not is_over: # if player jumped into normal square
            Entity.reward = Entity.reward_rubric["otherwise"] # that is -3 for existing
            Entity.score += Entity.reward
        return is_over


    def env_step(self, action):
        Entity.playerSteps += 1

        self.do_action(action)
        is_over = self.state_handler() 
        # if is_over:
        #     Entity.restart()
        #     # print(f"{Entity.reward} - <env_step>")
        state, reward = self.get_state(), Entity.reward
        return state, reward, is_over

    @classmethod
    def make_bombs(cls,num, player_ind):
        # uncomment
        allset = {i+1 for i in range(Entity.DIM**2-1)}
        forbid_set = {player_ind, Entity.entities[1].index}
        allowed = list(allset.difference(forbid_set))
        locations = [choice(allowed) for i in range(num)]
        
        # locations = [3, 9, 14, 7] # comment out
        for location in locations:
            Entity(location, Entity.identities[1])


    @classmethod
    def initialize_players(cls):
        player_ind, home_ind, bomb_num = cls.INIT_VARS
        Entity(player_ind, Entity.identities[0]) # squirrel
        Entity(home_ind, Entity.identities[2]) # home
        cls.make_bombs(bomb_num, player_ind) # make boobs haha
        

    def get_state(self) -> tuple:
        state = []
        if self.identitiy == "player":
            state.append(self.index)
            to_right, to_left, to_down = 0, 0, 0
            for entity in Entity.entities:
                if entity.identitiy == "bomb":
                    bomb = entity
                    if bomb.index == self.index + 1:
                        to_right = 1
                    elif bomb.index == self.index - 1:
                        to_left = 1
                    elif bomb.index == self.index + Entity.DIM:
                        to_down = 1
            state.extend([to_right, to_left, to_down])
            return tuple(state)
        else: return tuple()
            
                    # to_right = self.index + 1
                    # to_left = self.index - 1
                    # to_down = self.index + Entity.DIM
                    # checker = {
                    #     to_right: 0,
                    #     to_left : 0,
                    #     to_down : 0, 
                    #     }
                    # if bomb.index in checker.keys():
                    #     checker[entity.index] = 1

            # state.extend(list(checker.values()))
    
    # @classmethod
    # def show_render(render: bool):
    #     if render:
    #         FPS = 6
    #         pygame.init()
    #         screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #         clock = pygame.time.Clock()
    #         screen.fill(grey)
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 quit()
    #         draw_grid(screen, cell_width, DIM, white, 3)
            
    #         for entity in Entity.entities:
    #             color_table = {"player": gold, "bomb": red, "home": orange}
    #             color = color_table[entity.identitiy]
    #             pygame.draw.circle(screen, cell_width//3, color, cell_matrix[entity.index])
            
    #         pygame.display.flip()
    #         clock.tick(FPS)
    #     else:
#     #         pygame.quit()

# class Simulator(Entity):
#     WIDTH, HEIGHT = int(), int()
#     FPS = 6
#     grey = (37, 35, 35)
#     red = (255, 0 , 0)
#     white = (240, 240, 240)
#     gold = (250, 210, 20)
#     orange = (240, 150, 20)

#     @classmethod
#     def show_render(render: bool):
#         if render:
#             FPS = 6
#             pygame.init()
#             screen = pygame.display.set_mode((Simulator.WIDTH, Simulator.HEIGHT))
#             clock = pygame.time.Clock()
#             screen.fill(Simulator.grey)
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     quit()
#             draw_grid(screen, cell_width, DIM, white, 3)
            
#             for entity in Entity.entities:
#                 color_table = {"player": gold, "bomb": red, "home": orange}
#                 color = color_table[entity.identitiy]
#                 pygame.draw.circle(screen, cell_width//3, color, cell_matrix[entity.index])
            
#             pygame.display.flip()
#             clock.tick(FPS)
#         else:
#             pygame.quit()