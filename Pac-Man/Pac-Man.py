import random
from board import board
from copy import copy


class Game():
    def __init__(self):
        self.collision_dict = {
            "wall": "#",
            "point": ".",
            "fruit": "o",
            "void": " ",
            "wrap": "[",
            "door": "{",
            "pacman": "@"
        }
        self.ghost_list =["è","ç","à","&"]
        self.current_state = [15, 11]  # État actuel (ligne, colonne)
        self.previous_state = [15, 11]
        self.inky_previous_object = None
        self.inky_state = [15, 13] #[8, 10]
        self.blinky_state = [10, 9]
        self.pinky_state = [10, 10]
        self.clyde_state = [10, 11]
        self.score = 0 # 10*208 : . et 100*4 : o score totale
        self.done = False  # Indique si la partie est terminée
        self.board = board()
        self.board_ghost_check = board()
        self.board_size = [len(self.board),len(self.board[0])]
        self.initialize_position()
        self.generate_map()

    def step(self, action):
        if action == 0:
            self.pacmac(action)
            self.update_pacman_position(action)
            self.inky()
            self.update_inky_position()
            self.generate_map()

        elif action == 1:
            self.pacmac(action)
            self.update_pacman_position(action)
            self.inky()
            self.update_inky_position()
            self.generate_map()

        elif action == 2:
            self.pacmac(action)
            self.update_pacman_position(action)
            self.inky()
            self.update_inky_position()
            self.generate_map()

        elif action == 3:
            self.pacmac(action)
            self.update_pacman_position(action)
            self.inky()
            self.update_inky_position()
            self.generate_map()
        return self.current_state, self.score, self.done

    def move(self, x, y):
        action_0 = self.board[x - 1][y] # Haut
        action_1 = self.board[x + 1][y] # Bas
        action_2 = self.board[x][y - 1] # Gauche
        action_3 = self.board[x][y + 1] # Droite

        return action_0, action_1, action_2, action_3

    def pacmac(self, action):
        if action == 0:
            if self.move(self.current_state[0], self.current_state[1])[0] == self.collision_dict["wall"]:
                pass
            elif self.move(self.current_state[0], self.current_state[1])[0] == self.collision_dict["point"]:
                self.previous_state = copy(self.current_state)
                self.current_state[0] = self.current_state[0] - 1
                self.score += 10
            elif self.move(self.current_state[0], self.current_state[1])[0] == self.collision_dict["fruit"]:
                pass
            elif self.move(self.current_state[0], self.current_state[1])[0] == self.collision_dict["void"]:
                self.previous_state = copy(self.current_state)
                self.current_state[0] = self.current_state[0] - 1
            elif self.move(self.current_state[0], self.current_state[1])[0] == any(self.ghost_list) or self.score == 2480:
                self.done = True


        if action == 1:
            if self.move(self.current_state[0], self.current_state[1])[1] == self.collision_dict["wall"]:
                pass
            elif self.move(self.current_state[0], self.current_state[1])[1] == self.collision_dict["point"]:
                self.previous_state = copy(self.current_state)
                self.current_state[0] = self.current_state[0] + 1
                self.score += 10
            elif self.move(self.current_state[0], self.current_state[1])[1] == self.collision_dict["fruit"]:
                pass
            elif self.move(self.current_state[0], self.current_state[1])[1] == self.collision_dict["door"]:
                pass
            elif self.move(self.current_state[0], self.current_state[1])[1] == self.collision_dict["void"]:
                self.previous_state = copy(self.current_state)
                self.current_state[0] = self.current_state[0] + 1
            elif self.move(self.current_state[0], self.current_state[1])[1] == any(self.ghost_list) or self.score == 2480:
                self.done = True


        if action == 2:
            if self.move(self.current_state[0], self.current_state[1])[2] == self.collision_dict["wall"]:
                pass
            elif self.move(self.current_state[0], self.current_state[1])[2] == self.collision_dict["point"]:
                self.previous_state = copy(self.current_state)
                self.current_state[1] = self.current_state[1] - 1
                self.score += 10
            elif self.move(self.current_state[0], self.current_state[1])[2] == self.collision_dict["wrap"]:
                self.previous_state = copy(self.current_state)
                self.current_state = [10, 19]
            elif self.move(self.current_state[0], self.current_state[1])[2] == self.collision_dict["void"]:
                self.previous_state = copy(self.current_state)
                self.current_state[1] = self.current_state[1] - 1
            elif self.move(self.current_state[0], self.current_state[1])[2] == any(self.ghost_list) or self.score == 2480:
                self.done = True

        if action == 3:
            if self.move(self.current_state[0], self.current_state[1])[3] == self.collision_dict["wall"]:
                pass
            elif self.move(self.current_state[0], self.current_state[1])[3] == self.collision_dict["point"]:
                self.previous_state = copy(self.current_state)
                self.current_state[1] = self.current_state[1] + 1
                self.score += 10
            elif self.move(self.current_state[0], self.current_state[1])[3] == self.collision_dict["wrap"]:
                self.previous_state = copy(self.current_state)
                self.current_state = [10, 1]
            elif self.move(self.current_state[0], self.current_state[1])[3] == self.collision_dict["void"]:
                self.previous_state = copy(self.current_state)
                self.current_state[1] = self.current_state[1] + 1
            elif self.move(self.current_state[0], self.current_state[1])[3] == any(self.ghost_list) or self.score == 2480:
                self.done = True

    def update_pacman_position(self, action):
        if self.current_state == [10, 2] and action == 3:
            self.board[self.previous_state[0]][self.previous_state[1]] = "["
            self.board[self.current_state[0]][self.current_state[1]] = "@"

            self.board_ghost_check[self.previous_state[0]][self.previous_state[1]] = "["
            self.board_ghost_check[self.current_state[0]][self.current_state[1]] = "@"

        elif self.current_state == [10, 18] and action == 2:
            self.board[self.previous_state[0]][self.previous_state[1]] = "]"
            self.board[self.current_state[0]][self.current_state[1]] = "@"

            self.board_ghost_check[self.previous_state[0]][self.previous_state[1]] = "]"
            self.board_ghost_check[self.current_state[0]][self.current_state[1]] = "@"

        else:
            self.board[self.previous_state[0]][self.previous_state[1]] = " "
            self.board[self.current_state[0]][self.current_state[1]] = "@"

            self.board_ghost_check[self.previous_state[0]][self.previous_state[1]] = " "
            self.board_ghost_check[self.current_state[0]][self.current_state[1]] = "@"

    def inky(self):
        self.direction_inky = random.randint(0,3)
        self.inky_moving = True

        if self.direction_inky == 0:
            if self.move(self.inky_state[0], self.inky_state[1])[0] == self.collision_dict["wall"]:
                self.inky_moving = False
                pass
            elif self.move(self.inky_state[0], self.inky_state[1])[0] == self.collision_dict["pacman"]:
                self.done = True
            else:
                self.inky_previous_object = self.board_ghost_check[self.inky_state[0]][self.inky_state[1]]
                self.inky_previous_state = copy(self.inky_state)
                self.inky_state[0] = self.inky_state[0] - 1
                self.inky_moving = True

        if self.direction_inky == 1:
            if self.move(self.inky_state[0], self.inky_state[1])[1] == self.collision_dict["wall"]:
                self.inky_moving = False
                pass
            elif self.move(self.inky_state[0], self.inky_state[1])[1] == self.collision_dict["door"]:
                self.inky_moving = False
                pass
            elif self.move(self.inky_state[0], self.inky_state[1])[1] == self.collision_dict["pacman"]:
                self.done = True
            else:
                self.inky_previous_object = self.board_ghost_check[self.inky_state[0]][self.inky_state[1]]
                self.inky_previous_state = copy(self.inky_state)
                self.inky_state[0] = self.inky_state[0] + 1
                self.inky_moving = True

        if self.direction_inky == 2:
            if self.move(self.inky_state[0], self.inky_state[1])[2] == self.collision_dict["wall"]:
                self.inky_moving = False
                pass
            elif self.move(self.inky_state[0], self.inky_state[1])[2] == self.collision_dict["wrap"]:
                self.inky_previous_state = copy(self.direction_inky)
                self.inky_state = [10, 19]
                self.inky_moving = True
            elif self.move(self.inky_state[0], self.inky_state[1])[2] == self.collision_dict["pacman"]:
                self.done = True
            else:
                self.inky_previous_object = self.board_ghost_check[self.inky_state[0]][self.inky_state[1]]
                self.inky_previous_state = copy(self.inky_state)
                self.inky_state[1] = self.inky_state[1] - 1
                self.inky_moving = True

        if self.direction_inky == 3:
            if self.move(self.inky_state[0], self.inky_state[1])[3] == self.collision_dict["wall"]:
                self.inky_moving = False
                pass
            elif self.move(self.inky_state[0], self.inky_state[1])[3] == self.collision_dict["wrap"]:
                self.inky_previous_state = copy(self.direction_inky)
                self.inky_state = [10, 1]
                self.inky_moving = True
            elif self.move(self.inky_state[0], self.inky_state[1])[3] == self.collision_dict["pacman"]:
                self.done = True
            else:
                self.inky_previous_object = self.board_ghost_check[self.inky_state[0]][self.inky_state[1]]
                self.inky_previous_state = copy(self.inky_state)
                self.inky_state[1] = self.inky_state[1] + 1
                self.inky_moving = True
            
    def update_inky_position(self):
        if self.inky_state == [10, 2] and self.direction_inky == 3:
            self.board[self.inky_previous_state[0]][self.inky_previous_state[1]] = "["
            self.board[self.inky_state[0]][self.inky_state[1]] = "é"

        elif self.current_state == [10, 18] and self.direction_inky == 2:
            self.board[self.inky_previous_state[0]][self.inky_previous_state[1]] = "]"
            self.board[self.inky_state[0]][self.inky_state[1]] = "é"

        elif self.inky_moving == False :
            pass

        else:
            self.board[self.inky_previous_state[0]][self.inky_previous_state[1]] = self.inky_previous_object
            self.board[self.inky_state[0]][self.inky_state[1]] = "é"

    def generate_map(self):
        for i in self.board:
            print(*i, sep=' ')

    def initialize_position(self):
        self.board[self.current_state[0]][self.current_state[1]] = "@"
        self.board[self.inky_state[0]][self.inky_state[1]] = "é"
        self.board[self.blinky_state[0]][self.blinky_state[1]] = "ç"
        self.board[self.pinky_state[0]][self.pinky_state[1]] = "à"
        self.board[self.clyde_state[0]][self.clyde_state[1]] = "&"


if __name__ == '__main__':
    """
    Il faut choisir un nombre entre 0 et 3
    - Si l'action est 0, déplacement vers le haut
    - Si l'action est 1, déplacement vers le bas
    - Si l'action est 2, déplacement vers la gauche
    - Si l'action est 3, déplacement vers la droite 
    
    @ : PacMan / é, ç, à, & : fantome / #, |, - : murs / . : point / o : gros point 
    
    """

    world = Game()
    while world.done == False:
        print("-------------------------------------Next iteration-------------------------------------")
        world.step(random.randint(0,3))

    print("-------------------------------------La partie est terminée-------------------------------------")
    print("--------------------------Votre score est de: {}".format(world.score))
    if world.score == 2480:
        reward = 1000
    elif world.score != 2480:
        reward = -300

