from board import board
from copy import copy
class PacMan():
    def __init__(self):
        self.current_state = [15, 10]  # État actuel (ligne, colonne)
        self.previous_state = [15, 10]
        #self.end_good_state = good_end_position  # État final (ligne, colonne)
        #self.end_bad_state = bad_end_position
        self.num_actions = 4  # Nombre total d'actions possibles (haut, bas, gauche, droite)
        self.reward = 0  # Récompense actuelle
        self.score = 0 # 10 : . et 100 : o
        self.done = False  # Indique si la partie est terminée
        self.board = board()
        self.board_size = [len(self.board),len(self.board[0])]
        self.generate_map(None)

    def step(self, action):
        if action == 0 :
            self.collision(action)
            self.generate_map(action)

        elif action == 1 :
                self.collision(action)
                self.generate_map(action)

        elif action == 2 :
                self.collision(action)
                self.generate_map(action)

        elif action == 3 :
                self.collision(action)
                self.generate_map(action)

        return self.previous_state, self.current_state, self.done

    def move(self):
        action_0 = self.board[self.current_state[0] - 1][self.current_state[1]] # Haut
        action_1 = self.board[self.current_state[0] + 1][self.current_state[1]] # Bas
        action_2 = self.board[self.current_state[0]][self.current_state[1] - 1] # Gauche
        action_3 = self.board[self.current_state[0]][self.current_state[1] + 1] # Droite

        return action_0, action_1, action_2, action_3

    def collision(self, action):
        collision_dict = {
            "wall": "#",
            "point": ".",
            "fruit": "o",
            "void": " ",
            "wrap": "[",
            "door": "{"
        }
        if action == 0:
            if self.move()[0] == collision_dict["wall"]:
                pass
            elif self.move()[0] == collision_dict["point"]:
                self.previous_state = copy(self.current_state)
                self.current_state[0] = self.current_state[0] - 1
                self.score += 10
            elif self.move()[0] == collision_dict["fruit"]:
                pass
            elif self.move()[0] == collision_dict["void"]:
                self.previous_state = copy(self.current_state)
                self.current_state[0] = self.current_state[0] - 1


        if action == 1:
            if self.move()[1] == collision_dict["wall"]:
                pass
            elif self.move()[1] == collision_dict["point"]:
                self.previous_state = copy(self.current_state)
                self.current_state[0] = self.current_state[0] + 1
                self.score += 10
            elif self.move()[1] == collision_dict["fruit"]:
                pass
            elif self.move()[1] == collision_dict["door"]:
                pass
            elif self.move()[1] == collision_dict["void"]:
                self.previous_state = copy(self.current_state)
                self.current_state[0] = self.current_state[0] + 1


        if action == 2:
            if self.move()[2] == collision_dict["wall"]:
                pass
            elif self.move()[2] == collision_dict["point"]:
                self.previous_state = copy(self.current_state)
                self.current_state[1] = self.current_state[1] - 1
                self.score += 10
            elif self.move()[2] == collision_dict["wrap"]:
                self.previous_state = copy(self.current_state)
                self.current_state = [10, 18]
            elif self.move()[2] == collision_dict["void"]:
                self.previous_state = copy(self.current_state)
                self.current_state[1] = self.current_state[1] - 1


        if action == 3:
            if self.move()[3] == collision_dict["wall"]:
                pass
            elif self.move()[3] == collision_dict["point"]:
                self.previous_state = copy(self.current_state)
                self.current_state[1] = self.current_state[1] + 1
                self.score += 10
            elif self.move()[3] == collision_dict["wrap"]:
                self.previous_state = copy(self.current_state)
                self.current_state = [10, 1]
            elif self.move()[3] == collision_dict["void"]:
                self.previous_state = copy(self.current_state)
                self.current_state[1] = self.current_state[1] + 1


    def generate_map(self, action):
        if self.current_state == [10, 2] and action == 3:
            self.board[self.previous_state[0]][self.previous_state[1]] = "["
            self.board[self.current_state[0]][self.current_state[1]] = "@"
            for i in self.board:
                print(*i, sep=' ')
        elif self.current_state == [10, 17] and action == 2:
            self.board[self.previous_state[0]][self.previous_state[1]] = "]"
            self.board[self.current_state[0]][self.current_state[1]] = "@"
            for i in self.board:
                print(*i, sep=' ')
        else:
            self.board[self.previous_state[0]][self.previous_state[1]] = " "
            self.board[self.current_state[0]][self.current_state[1]] = "@"
            for i in self.board:
                print(*i, sep=' ')





if __name__ == '__main__':
    """
    Il faut choisir un nombre entre 0 et 3
    - Si l'action est 0, déplacement vers le haut
    - Si l'action est 1, déplacement vers le bas
    - Si l'action est 2, déplacement vers la gauche
    - Si l'action est 3, déplacement vers la droite 
    
    @ : PacMan / é, ç, à, & : fantome / #, |, - : murs / . : point / o : gros point 
    
    """

    world = PacMan()
    print("-------------------------------------Next iteration-------------------------------------")
    world.step(3)
    print("-------------------------------------Next iteration-------------------------------------")
    world.step(3)
    print("-------------------------------------Next iteration-------------------------------------")
    world.step(0)