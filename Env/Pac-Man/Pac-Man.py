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
        self.ghost_list = ["è", "ç", "à", "&"]
        """
        //Characters
        """
        self.current_state = [15, 11]  # État actuel (ligne, colonne)
        self.previous_state = [15, 11]

        self.inky_state = [8, 10]  # [8, 10]
        self.inky_previous_object = None
        self.killable_inky = False
        self.inky_killed = False

        self.blinky_state = [10, 9]
        self.blinky_previous_object = None
        self.killable_blinky = False
        self.blinky_killed = False

        self.pinky_state = [10, 10]
        self.pinky_previous_object = None
        self.killable_pinky = False
        self.pinky_killed = False

        self.clyde_state = [10, 11]
        self.clyde_previous_object = None
        self.killable_clyde = False
        self.clyde_killed = False

        """
        // Game
        """
        self.score = 0  # 10*208 : . et 100*4 : o score totale
        self.done = False  # Indique si la partie est terminée
        self.board = board()
        self.board_ghost_check = board()
        self.board_size = [len(self.board), len(self.board[0])]
        self.compteur_first_step = 0
        self.compteur_ghost = 0
        self.fruit_collision = False
        self.initialize_position()
        self.generate_map()

    def chose_next_move(self):
        if self.compteur_first_step <= 3:
            chose_inky = [2, 2, 0, 0]
            chose_blinky = [2, 3, 0, 3]
            chose_pinky = [0, 3, 3, 3]
            chose_clyde = [2, 0, 2, 2]
            self.chose_inky, self.chose_blinky, self.chose_pinky, self.chose_clyde = chose_inky[
                                                                                         self.compteur_first_step], \
                                                                                     chose_blinky[
                                                                                         self.compteur_first_step], \
                                                                                     chose_pinky[
                                                                                         self.compteur_first_step], \
                                                                                     chose_clyde[
                                                                                         self.compteur_first_step]
            self.compteur_first_step += 1

        elif self.compteur_first_step > 3:
            self.chose_inky = random.randint(0, 3)
            self.chose_blinky = random.randint(0, 3)
            self.chose_pinky = random.randint(0, 3)
            self.chose_clyde = random.randint(0, 3)

    def action(self, action):
        self.chose_next_move()
        self.pacmac(action)
        self.update_pacman_position(action)
        self.timer_fruit()

        self.inky(self.chose_inky)
        self.update_inky_position(self.chose_inky)

        self.pinky(self.chose_pinky)
        self.update_pinky_position(self.chose_pinky)

        self.clyde(self.chose_clyde)
        self.update_clyde_position(self.chose_clyde)

        self.blinky(self.chose_blinky)
        self.update_blinky_position(self.chose_blinky)

        self.generate_map()

    def step(self, action):  # Action de Pac-man
        if action == 0:
            self.action(action)

        elif action == 1:
            self.action(action)

        elif action == 2:
            self.action(action)

        elif action == 3:
            self.action(action)

        return self.current_state, self.score, self.done

    def move(self, x, y):
        action_0 = self.board[x - 1][y]  # Haut
        action_1 = self.board[x + 1][y]  # Bas
        action_2 = self.board[x][y - 1]  # Gauche
        action_3 = self.board[x][y + 1]  # Droite

        return action_0, action_1, action_2, action_3

    def match_ghost_and_state(self, object_to_match):
        if object_to_match == self.ghost_list[0]:
            self.inky_killed = True
        elif object_to_match == self.ghost_list[1]:
            self.blinky_killed = True
        elif object_to_match == self.ghost_list[2]:
            self.pinky_killed = True
        elif object_to_match == self.ghost_list[3]:
            self.clyde_killed = True

    def update_score_move_from_ghost(self):
        if self.inky_previous_object == ".":
            self.previous_state = copy(self.current_state)
            self.current_state[0] = self.current_state[0] - 1
            self.score += 10
        elif self.inky_previous_object == "o":
            self.previous_state = copy(self.current_state)
            self.current_state[0] = self.current_state[0] - 1
            self.score += 100
        elif self.inky_previous_object == " ":
            self.previous_state = copy(self.current_state)
            self.current_state[0] = self.current_state[0] - 1

    def timer_fruit(self):
        if self.compteur_ghost > 4:
            self.fruit_collision = False
            self.compteur_ghost = 0
            self.killable_inky = False
            self.killable_pinky = False
            self.killable_blinky = False
            self.killable_clyde = False
            self.fruit_collision = False
        elif self.fruit_collision == True and self.compteur_ghost < 5:
            self.compteur_ghost += 1

    """
    ---------------------------------------------------------
    //PACMAN
    ---------------------------------------------------------
    """

    def pacmac(self, action):
        if self.score == 2500:
            self.done = True
        else:
            if action == 0:
                haut = self.move(self.current_state[0], self.current_state[1])[0]
                if haut == self.collision_dict["wall"]:
                    pass
                elif haut == self.collision_dict["point"]:
                    self.previous_state = copy(self.current_state)
                    self.current_state[0] = self.current_state[0] - 1
                    self.score += 10
                elif haut == self.collision_dict["fruit"]:
                    self.previous_state = copy(self.current_state)
                    self.current_state[0] = self.current_state[0] - 1
                    self.score += 100
                    self.killable_inky = True
                    self.killable_pinky = True
                    self.killable_blinky = True
                    self.killable_clyde = True
                    self.fruit_collision = True
                    self.compteur_ghost = 0
                elif haut == self.collision_dict["void"]:
                    self.previous_state = copy(self.current_state)
                    self.current_state[0] = self.current_state[0] - 1
                elif haut == any(self.ghost_list):
                    if self.killable_inky or self.killable_pinky or self.killable_blinky or self.killable_clyde == False:
                        self.done = True
                    elif self.killable_inky or self.killable_pinky or self.killable_blinky or self.killable_clyde == True:
                        self.match_ghost_and_state(haut)
                        self.update_score_move_from_ghost()

            if action == 1:
                bas = self.move(self.current_state[0], self.current_state[1])[1]
                if bas == self.collision_dict["wall"]:
                    pass
                elif bas == self.collision_dict["point"]:
                    self.previous_state = copy(self.current_state)
                    self.current_state[0] = self.current_state[0] + 1
                    self.score += 10
                elif bas == self.collision_dict["fruit"]:
                    self.previous_state = copy(self.current_state)
                    self.current_state[0] = self.current_state[0] + 1
                    self.score += 100
                    self.killable_inky = True
                    self.killable_pinky = True
                    self.killable_blinky = True
                    self.killable_clyde = True
                    self.fruit_collision = True
                    self.compteur_ghost = 0
                elif bas == self.collision_dict["door"]:
                    pass
                elif bas == self.collision_dict["void"]:
                    self.previous_state = copy(self.current_state)
                    self.current_state[0] = self.current_state[0] + 1
                elif bas == any(self.ghost_list):
                    if self.killable_inky or self.killable_pinky or self.killable_blinky or self.killable_clyde == False:
                        self.done = True
                    elif self.killable_inky or self.killable_pinky or self.killable_blinky or self.killable_clyde == True:
                        self.match_ghost_and_state(bas)
                        self.update_score_move_from_ghost()

            if action == 2:
                gauche = self.move(self.current_state[0], self.current_state[1])[2]
                if gauche == self.collision_dict["wall"]:
                    pass
                elif gauche == self.collision_dict["point"]:
                    self.previous_state = copy(self.current_state)
                    self.current_state[1] = self.current_state[1] - 1
                    self.score += 10
                elif gauche == self.collision_dict["wrap"]:
                    self.previous_state = copy(self.current_state)
                    self.current_state = [10, 19]
                elif gauche == self.collision_dict["void"]:
                    self.previous_state = copy(self.current_state)
                    self.current_state[1] = self.current_state[1] - 1
                elif gauche == any(self.ghost_list):
                    if self.killable_inky or self.killable_pinky or self.killable_blinky or self.killable_clyde == False:
                        self.done = True
                    elif self.killable_inky or self.killable_pinky or self.killable_blinky or self.killable_clyde == True:
                        self.match_ghost_and_state(gauche)
                        self.update_score_move_from_ghost()

            if action == 3:
                droite = self.move(self.current_state[0], self.current_state[1])[3]
                if droite == self.collision_dict["wall"]:
                    pass
                elif droite == self.collision_dict["point"]:
                    self.previous_state = copy(self.current_state)
                    self.current_state[1] = self.current_state[1] + 1
                    self.score += 10
                elif droite == self.collision_dict["wrap"]:
                    self.previous_state = copy(self.current_state)
                    self.current_state = [10, 1]
                elif droite == self.collision_dict["void"]:
                    self.previous_state = copy(self.current_state)
                    self.current_state[1] = self.current_state[1] + 1
                elif droite == any(self.ghost_list):
                    if self.killable_inky or self.killable_pinky or self.killable_blinky or self.killable_clyde == False:
                        self.done = True
                    elif self.killable_inky or self.killable_pinky or self.killable_blinky or self.killable_clyde == True:
                        self.match_ghost_and_state(droite)
                        self.update_score_move_from_ghost()

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

    """
    ---------------------------------------------------------
    //INKY
    ---------------------------------------------------------
    """

    def inky(self, direction_inky):
        if self.inky_killed == False:
            self.inky_moving = True
            if direction_inky == 0:
                if self.move(self.inky_state[0], self.inky_state[1])[0] == self.collision_dict["wall"]:
                    self.inky_moving = False
                    pass
                elif self.move(self.inky_state[0], self.inky_state[1])[0] == self.collision_dict["pacman"]:
                    if self.killable_inky == False:
                        self.done = True
                    elif self.killable_inky == True:
                        if self.inky_previous_object == ".":
                            self.inky_killed = True
                            self.inky_moving = False
                            self.score += 10
                        elif self.inky_previous_object == "o":
                            self.inky_killed = True
                            self.inky_moving = False
                            # setup killable
                            self.score += 100
                        elif self.inky_previous_object == " ":
                            self.inky_killed = True
                            self.inky_moving = False
                            # setup killable
                else:
                    self.inky_previous_object = self.board_ghost_check[self.inky_state[0]][self.inky_state[1]]
                    self.inky_previous_state = copy(self.inky_state)
                    self.inky_state[0] = self.inky_state[0] - 1
                    self.inky_moving = True

            if direction_inky == 1:
                if self.move(self.inky_state[0], self.inky_state[1])[1] == self.collision_dict["wall"]:
                    self.inky_moving = False
                    pass
                elif self.move(self.inky_state[0], self.inky_state[1])[1] == self.collision_dict["door"]:
                    self.inky_moving = False
                    pass
                elif self.move(self.inky_state[0], self.inky_state[1])[1] == self.collision_dict["pacman"]:
                    if self.killable_inky == False:
                        self.done = True
                    elif self.killable_inky == True:
                        if self.inky_previous_object == ".":
                            self.inky_killed = True
                            self.inky_moving = False
                            self.score += 10
                        elif self.inky_previous_object == "o":
                            self.inky_killed = True
                            self.inky_moving = False
                            # setup killable
                            self.score += 100
                        elif self.inky_previous_object == " ":
                            self.inky_killed = True
                            self.inky_moving = False
                            # setup killable
                else:
                    self.inky_previous_object = self.board_ghost_check[self.inky_state[0]][self.inky_state[1]]
                    self.inky_previous_state = copy(self.inky_state)
                    self.inky_state[0] = self.inky_state[0] + 1
                    self.inky_moving = True

            if direction_inky == 2:
                if self.move(self.inky_state[0], self.inky_state[1])[2] == self.collision_dict["wall"]:
                    self.inky_moving = False
                    pass
                elif self.move(self.inky_state[0], self.inky_state[1])[2] == self.collision_dict["wrap"]:
                    self.inky_previous_state = copy(direction_inky)
                    self.inky_state = [10, 19]
                    self.inky_moving = True
                elif self.move(self.inky_state[0], self.inky_state[1])[2] == self.collision_dict["pacman"]:
                    if self.killable_inky == False:
                        self.done = True
                    elif self.killable_inky == True:
                        if self.inky_previous_object == ".":
                            self.inky_killed = True
                            self.inky_moving = False
                            self.score += 10
                        elif self.inky_previous_object == "o":
                            self.inky_killed = True
                            self.inky_moving = False
                            # setup killable
                            self.score += 100
                        elif self.inky_previous_object == " ":
                            self.inky_killed = True
                            self.inky_moving = False
                            # setup killable
                else:
                    self.inky_previous_object = self.board_ghost_check[self.inky_state[0]][self.inky_state[1]]
                    self.inky_previous_state = copy(self.inky_state)
                    self.inky_state[1] = self.inky_state[1] - 1
                    self.inky_moving = True

            if direction_inky == 3:
                if self.move(self.inky_state[0], self.inky_state[1])[3] == self.collision_dict["wall"]:
                    self.inky_moving = False
                    pass
                elif self.move(self.inky_state[0], self.inky_state[1])[3] == self.collision_dict["wrap"]:
                    self.inky_previous_state = copy(direction_inky)
                    self.inky_state = [10, 1]
                    self.inky_moving = True
                elif self.move(self.inky_state[0], self.inky_state[1])[3] == self.collision_dict["pacman"]:
                    if self.killable_inky == False:
                        self.done = True
                    elif self.killable_inky == True:
                        if self.inky_previous_object == ".":
                            self.inky_killed = True
                            self.inky_moving = False
                            self.score += 10
                        elif self.inky_previous_object == "o":
                            self.inky_killed = True
                            self.inky_moving = False
                            # setup killable
                            self.score += 100
                        elif self.inky_previous_object == " ":
                            self.inky_killed = True
                            self.inky_moving = False
                            # setup killable
                else:
                    self.inky_previous_object = self.board_ghost_check[self.inky_state[0]][self.inky_state[1]]
                    self.inky_previous_state = copy(self.inky_state)
                    self.inky_state[1] = self.inky_state[1] + 1
                    self.inky_moving = True
        elif self.inky_killed == True:
            pass

    def update_inky_position(self, direction_inky):
        if self.inky_killed == False:
            if self.inky_state == [10, 2] and direction_inky == 3:
                self.board[self.inky_previous_state[0]][self.inky_previous_state[1]] = "["
                self.board[self.inky_state[0]][self.inky_state[1]] = "é"

            elif self.current_state == [10, 18] and direction_inky == 2:
                self.board[self.inky_previous_state[0]][self.inky_previous_state[1]] = "]"
                self.board[self.inky_state[0]][self.inky_state[1]] = "é"

            elif self.inky_moving == False:
                pass

            else:
                self.board[self.inky_previous_state[0]][self.inky_previous_state[1]] = self.inky_previous_object
                self.board[self.inky_state[0]][self.inky_state[1]] = "é"
        elif self.inky_killed == True:
            if self.board[self.inky_state[0]][self.inky_state[1]] != "é":
                pass
            elif self.board[self.inky_state[0]][self.inky_state[1]] == "é":
                self.board[self.inky_state[0]][self.inky_state[1]] = self.inky_previous_object

    """
    ---------------------------------------------------------
    //BLINKY
    ---------------------------------------------------------
    """

    def blinky(self, direction_blinky):
        if self.blinky_killed == False:
            self.blinky_moving = True
            if direction_blinky == 0:
                if self.move(self.blinky_state[0], self.blinky_state[1])[0] == self.collision_dict["wall"]:
                    self.blinky_moving = False
                    pass
                elif self.move(self.blinky_state[0], self.blinky_state[1])[0] == self.collision_dict["pacman"]:
                    if self.killable_blinky == False:
                        self.done = True
                    elif self.killable_blinky == True:
                        if self.blinky_previous_object == ".":
                            self.blinky_killed = True
                            self.blinky_moving = False
                            self.score += 10
                        elif self.blinky_previous_object == "o":
                            self.blinky_killed = True
                            self.blinky_moving = False
                            # setup killable
                            self.score += 100
                        elif self.blinky_previous_object == " ":
                            self.blinky_killed = True
                            self.blinky_moving = False
                            # setup killable
                elif self.move(self.blinky_state[0], self.blinky_state[1])[0] == self.collision_dict["door"]:
                    self.blinky_previous_object = self.board_ghost_check[self.blinky_state[0]][self.blinky_state[1]]
                    self.blinky_previous_state = copy(self.blinky_state)
                    self.blinky_state[0] = self.blinky_state[0] - 2
                    self.blinky_moving = True
                else:
                    self.blinky_previous_object = self.board_ghost_check[self.blinky_state[0]][self.blinky_state[1]]
                    self.blinky_previous_state = copy(self.blinky_state)
                    self.blinky_state[0] = self.blinky_state[0] - 1
                    self.blinky_moving = True

            if direction_blinky == 1:
                if self.move(self.blinky_state[0], self.blinky_state[1])[1] == self.collision_dict["wall"]:
                    self.blinky_moving = False
                    pass
                elif self.move(self.blinky_state[0], self.blinky_state[1])[1] == self.collision_dict["door"]:
                    self.blinky_moving = False
                    pass
                elif self.move(self.blinky_state[0], self.blinky_state[1])[1] == self.collision_dict["pacman"]:
                    if self.killable_blinky == False:
                        self.done = True
                    elif self.killable_blinky == True:
                        if self.blinky_previous_object == ".":
                            self.blinky_killed = True
                            self.blinky_moving = False
                            self.score += 10
                        elif self.blinky_previous_object == "o":
                            self.blinky_killed = True
                            self.blinky_moving = False
                            # setup killable
                            self.score += 100
                        elif self.blinky_previous_object == " ":
                            self.blinky_killed = True
                            self.blinky_moving = False
                            # setup killable
                else:
                    self.blinky_previous_object = self.board_ghost_check[self.blinky_state[0]][self.blinky_state[1]]
                    self.blinky_previous_state = copy(self.blinky_state)
                    self.blinky_state[0] = self.blinky_state[0] + 1
                    self.blinky_moving = True

            if direction_blinky == 2:
                if self.move(self.blinky_state[0], self.blinky_state[1])[2] == self.collision_dict["wall"]:
                    self.blinky_moving = False
                    pass
                elif self.move(self.blinky_state[0], self.blinky_state[1])[2] == self.collision_dict["wrap"]:
                    self.blinky_previous_state = copy(direction_blinky)
                    self.blinky_state = [10, 19]
                    self.blinky_moving = True
                elif self.move(self.blinky_state[0], self.blinky_state[1])[2] == self.collision_dict["pacman"]:
                    if self.killable_blinky == False:
                        self.done = True
                    elif self.killable_blinky == True:
                        if self.blinky_previous_object == ".":
                            self.blinky_killed = True
                            self.blinky_moving = False
                            self.score += 10
                        elif self.blinky_previous_object == "o":
                            self.blinky_killed = True
                            self.blinky_moving = False
                            # setup killable
                            self.score += 100
                        elif self.blinky_previous_object == " ":
                            self.blinky_killed = True
                            self.blinky_moving = False
                            # setup killable
                else:
                    self.blinky_previous_object = self.board_ghost_check[self.blinky_state[0]][self.blinky_state[1]]
                    self.blinky_previous_state = copy(self.blinky_state)
                    self.blinky_state[1] = self.blinky_state[1] - 1
                    self.blinky_moving = True

            if direction_blinky == 3:
                if self.move(self.blinky_state[0], self.blinky_state[1])[3] == self.collision_dict["wall"]:
                    self.blinky_moving = False
                    pass
                elif self.move(self.blinky_state[0], self.blinky_state[1])[3] == self.collision_dict["wrap"]:
                    self.blinky_previous_state = copy(direction_blinky)
                    self.blinky_state = [10, 1]
                    self.blinky_moving = True
                elif self.move(self.blinky_state[0], self.blinky_state[1])[3] == self.collision_dict["pacman"]:
                    if self.killable_blinky == False:
                        self.done = True
                    elif self.killable_blinky == True:
                        if self.blinky_previous_object == ".":
                            self.blinky_killed = True
                            self.blinky_moving = False
                            self.score += 10
                        elif self.blinky_previous_object == "o":
                            self.blinky_killed = True
                            self.blinky_moving = False
                            # setup killable
                            self.score += 100
                        elif self.blinky_previous_object == " ":
                            self.blinky_killed = True
                            self.blinky_moving = False
                            # setup killable
                else:
                    self.blinky_previous_object = self.board_ghost_check[self.blinky_state[0]][self.blinky_state[1]]
                    self.blinky_previous_state = copy(self.blinky_state)
                    self.blinky_state[1] = self.blinky_state[1] + 1
                    self.blinky_moving = True
        elif self.blinky_killed == True:
            pass

    def update_blinky_position(self, direction_blinky):
        if self.blinky_killed == False:
            if self.blinky_state == [10, 2] and direction_blinky == 3:
                self.board[self.blinky_previous_state[0]][self.blinky_previous_state[1]] = "["
                self.board[self.blinky_state[0]][self.blinky_state[1]] = "ç"

            elif self.blinky_state == [10, 18] and direction_blinky == 2:
                self.board[self.blinky_previous_state[0]][self.blinky_previous_state[1]] = "]"
                self.board[self.blinky_state[0]][self.blinky_state[1]] = "ç"

            elif self.blinky_moving == False:
                pass

            else:
                self.board[self.blinky_previous_state[0]][self.blinky_previous_state[1]] = self.blinky_previous_object
                self.board[self.blinky_state[0]][self.blinky_state[1]] = "ç"
        elif self.blinky_killed == True:
            if self.board[self.blinky_state[0]][self.blinky_state[1]] != "ç":
                pass
            elif self.board[self.blinky_state[0]][self.blinky_state[1]] == "ç":
                self.board[self.blinky_state[0]][self.blinky_state[1]] = self.blinky_previous_object

    """
    ---------------------------------------------------------
    //PINKY
    ---------------------------------------------------------
    """

    def pinky(self, direction_pinky):
        if self.pinky_killed == False:
            self.pinky_moving = True
            if direction_pinky == 0:
                if self.move(self.pinky_state[0], self.pinky_state[1])[0] == self.collision_dict["wall"]:
                    self.pinky_moving = False
                    pass
                elif self.move(self.pinky_state[0], self.pinky_state[1])[0] == self.collision_dict["pacman"]:
                    if self.killable_pinky == False:
                        self.done = True
                    elif self.killable_pinky == True:
                        if self.pinky_previous_object == ".":
                            self.pinky_killed = True
                            self.pinky_moving = False
                            self.score += 10
                        elif self.pinky_previous_object == "o":
                            self.pinky_killed = True
                            self.pinky_moving = False
                            # setup killable
                            self.score += 100
                        elif self.pinky_previous_object == " ":
                            self.pinky_killed = True
                            self.pinky_moving = False
                            # setup killable
                elif self.move(self.pinky_state[0], self.pinky_state[1])[0] == self.collision_dict["door"]:
                    self.pinky_previous_object = self.board_ghost_check[self.pinky_state[0]][self.pinky_state[1]]
                    self.pinky_previous_state = copy(self.pinky_state)
                    self.pinky_state[0] = self.pinky_state[0] - 2
                    self.pinky_moving = True
                else:
                    self.pinky_previous_object = self.board_ghost_check[self.pinky_state[0]][self.pinky_state[1]]
                    self.pinky_previous_state = copy(self.pinky_state)
                    self.pinky_state[0] = self.pinky_state[0] - 1
                    self.pinky_moving = True

            if direction_pinky == 1:
                if self.move(self.pinky_state[0], self.pinky_state[1])[1] == self.collision_dict["wall"]:
                    self.pinky_moving = False
                    pass
                elif self.move(self.pinky_state[0], self.pinky_state[1])[1] == self.collision_dict["door"]:
                    self.pinky_moving = False
                    pass
                elif self.move(self.pinky_state[0], self.pinky_state[1])[1] == self.collision_dict["pacman"]:
                    if self.killable_pinky == False:
                        self.done = True
                    elif self.killable_pinky == True:
                        if self.pinky_previous_object == ".":
                            self.pinky_killed = True
                            self.pinky_moving = False
                            self.score += 10
                        elif self.pinky_previous_object == "o":
                            self.pinky_killed = True
                            self.pinky_moving = False
                            # setup killable
                            self.score += 100
                        elif self.pinky_previous_object == " ":
                            self.pinky_killed = True
                            self.pinky_moving = False
                            # setup killable
                else:
                    self.pinky_previous_object = self.board_ghost_check[self.pinky_state[0]][self.pinky_state[1]]
                    self.pinky_previous_state = copy(self.pinky_state)
                    self.pinky_state[0] = self.pinky_state[0] + 1
                    self.pinky_moving = True

            if direction_pinky == 2:
                if self.move(self.pinky_state[0], self.pinky_state[1])[2] == self.collision_dict["wall"]:
                    self.pinky_moving = False
                    pass
                elif self.move(self.pinky_state[0], self.pinky_state[1])[2] == self.collision_dict["wrap"]:
                    self.pinky_previous_state = copy(direction_pinky)
                    self.pinky_state = [10, 19]
                    self.pinky_moving = True
                elif self.move(self.pinky_state[0], self.pinky_state[1])[2] == self.collision_dict["pacman"]:
                    if self.killable_pinky == False:
                        self.done = True
                    elif self.killable_pinky == True:
                        if self.pinky_previous_object == ".":
                            self.pinky_killed = True
                            self.pinky_moving = False
                            self.score += 10
                        elif self.pinky_previous_object == "o":
                            self.pinky_killed = True
                            self.pinky_moving = False
                            # setup killable
                            self.score += 100
                        elif self.pinky_previous_object == " ":
                            self.pinky_killed = True
                            self.pinky_moving = False
                            # setup killable
                else:
                    self.pinky_previous_object = self.board_ghost_check[self.pinky_state[0]][self.pinky_state[1]]
                    self.pinky_previous_state = copy(self.pinky_state)
                    self.pinky_state[1] = self.pinky_state[1] - 1
                    self.pinky_moving = True

            if direction_pinky == 3:
                if self.move(self.pinky_state[0], self.pinky_state[1])[3] == self.collision_dict["wall"]:
                    self.pinky_moving = False
                    pass
                elif self.move(self.pinky_state[0], self.pinky_state[1])[3] == self.collision_dict["wrap"]:
                    self.pinky_previous_state = copy(direction_pinky)
                    self.pinky_state = [10, 1]
                    self.pinky_moving = True
                elif self.move(self.pinky_state[0], self.pinky_state[1])[3] == self.collision_dict["pacman"]:
                    if self.killable_pinky == False:
                        self.done = True
                    elif self.killable_pinky == True:
                        if self.pinky_previous_object == ".":
                            self.pinky_killed = True
                            self.pinky_moving = False
                            self.score += 10
                        elif self.pinky_previous_object == "o":
                            self.pinky_killed = True
                            self.pinky_moving = False
                            # setup killable
                            self.score += 100
                        elif self.pinky_previous_object == " ":
                            self.pinky_killed = True
                            self.pinky_moving = False
                            # setup killable
                else:
                    self.pinky_previous_object = self.board_ghost_check[self.pinky_state[0]][self.pinky_state[1]]
                    self.pinky_previous_state = copy(self.pinky_state)
                    self.pinky_state[1] = self.pinky_state[1] + 1
                    self.pinky_moving = True
        elif self.pinky_killed == True:
            pass

    def update_pinky_position(self, direction_pinky):
        if self.pinky_killed == False:
            if self.pinky_state == [10, 2] and direction_pinky == 3:
                self.board[self.pinky_previous_state[0]][self.pinky_previous_state[1]] = "["
                self.board[self.pinky_state[0]][self.pinky_state[1]] = "à"

            elif self.pinky_state == [10, 18] and direction_pinky == 2:
                self.board[self.pinky_previous_state[0]][self.pinky_previous_state[1]] = "]"
                self.board[self.pinky_state[0]][self.pinky_state[1]] = "à"

            elif self.pinky_moving == False:
                pass

            else:
                self.board[self.pinky_previous_state[0]][self.pinky_previous_state[1]] = self.pinky_previous_object
                self.board[self.pinky_state[0]][self.pinky_state[1]] = "à"
        elif self.pinky_killed == True:
            if self.board[self.pinky_state[0]][self.pinky_state[1]] != "à":
                pass
            elif self.board[self.pinky_state[0]][self.pinky_state[1]] == "à":
                self.board[self.pinky_state[0]][self.pinky_state[1]] = self.pinky_previous_object

    """
    ---------------------------------------------------------
    //CLYDE
    ---------------------------------------------------------
    """

    def clyde(self, direction_clyde):
        if self.clyde_killed == False:
            self.clyde_moving = True
            if direction_clyde == 0:
                if self.move(self.clyde_state[0], self.clyde_state[1])[0] == self.collision_dict["wall"]:
                    self.clyde_moving = False
                    pass
                elif self.move(self.clyde_state[0], self.clyde_state[1])[0] == self.collision_dict["pacman"]:
                    if self.killable_clyde == False:
                        self.done = True
                    elif self.killable_clyde == True:
                        if self.clyde_previous_object == ".":
                            self.clyde_killed = True
                            self.clyde_moving = False
                            self.score += 10
                        elif self.clyde_previous_object == "o":
                            self.clyde_killed = True
                            self.clyde_moving = False
                            # setup killable
                            self.score += 100
                        elif self.clyde_previous_object == " ":
                            self.clyde_killed = True
                            self.clyde_moving = False
                            # setup killable
                elif self.move(self.clyde_state[0], self.clyde_state[1])[0] == self.collision_dict["door"]:
                    self.clyde_previous_object = self.board_ghost_check[self.clyde_state[0]][self.clyde_state[1]]
                    self.clyde_previous_state = copy(self.clyde_state)
                    self.clyde_state[0] = self.clyde_state[0] - 2
                    self.clyde_moving = True
                else:
                    self.clyde_previous_object = self.board_ghost_check[self.clyde_state[0]][self.clyde_state[1]]
                    self.clyde_previous_state = copy(self.clyde_state)
                    self.clyde_state[0] = self.clyde_state[0] - 1
                    self.clyde_moving = True

            if direction_clyde == 1:
                if self.move(self.clyde_state[0], self.clyde_state[1])[1] == self.collision_dict["wall"]:
                    self.clyde_moving = False
                    pass
                elif self.move(self.clyde_state[0], self.clyde_state[1])[1] == self.collision_dict["door"]:
                    self.clyde_moving = False
                    pass
                elif self.move(self.clyde_state[0], self.clyde_state[1])[1] == self.collision_dict["pacman"]:
                    if self.killable_clyde == False:
                        self.done = True
                    elif self.killable_clyde == True:
                        if self.clyde_previous_object == ".":
                            self.clyde_killed = True
                            self.clyde_moving = False
                            self.score += 10
                        elif self.clyde_previous_object == "o":
                            self.clyde_killed = True
                            self.clyde_moving = False
                            # setup killable
                            self.score += 100
                        elif self.clyde_previous_object == " ":
                            self.clyde_killed = True
                            self.clyde_moving = False
                            # setup killable
                else:
                    self.clyde_previous_object = self.board_ghost_check[self.clyde_state[0]][self.clyde_state[1]]
                    self.clyde_previous_state = copy(self.clyde_state)
                    self.clyde_state[0] = self.clyde_state[0] + 1
                    self.clyde_moving = True

            if direction_clyde == 2:
                if self.move(self.clyde_state[0], self.clyde_state[1])[2] == self.collision_dict["wall"]:
                    self.clyde_moving = False
                    pass
                elif self.move(self.clyde_state[0], self.clyde_state[1])[2] == self.collision_dict["wrap"]:
                    self.clyde_previous_state = copy(direction_clyde)
                    self.clyde_state = [10, 19]
                    self.clyde_moving = True
                elif self.move(self.clyde_state[0], self.clyde_state[1])[2] == self.collision_dict["pacman"]:
                    if self.killable_clyde == False:
                        self.done = True
                    elif self.killable_clyde == True:
                        if self.clyde_previous_object == ".":
                            self.clyde_killed = True
                            self.clyde_moving = False
                            self.score += 10
                        elif self.clyde_previous_object == "o":
                            self.clyde_killed = True
                            self.clyde_moving = False
                            # setup killable
                            self.score += 100
                        elif self.clyde_previous_object == " ":
                            self.clyde_killed = True
                            self.clyde_moving = False
                            # setup killable
                else:
                    self.clyde_previous_object = self.board_ghost_check[self.clyde_state[0]][self.clyde_state[1]]
                    self.clyde_previous_state = copy(self.clyde_state)
                    self.clyde_state[1] = self.clyde_state[1] - 1
                    self.clyde_moving = True

            if direction_clyde == 3:
                if self.move(self.clyde_state[0], self.clyde_state[1])[3] == self.collision_dict["wall"]:
                    self.clyde_moving = False
                    pass
                elif self.move(self.clyde_state[0], self.clyde_state[1])[3] == self.collision_dict["wrap"]:
                    self.clyde_previous_state = copy(direction_clyde)
                    self.clyde_state = [10, 1]
                    self.clyde_moving = True
                elif self.move(self.clyde_state[0], self.clyde_state[1])[3] == self.collision_dict["pacman"]:
                    if self.killable_clyde == False:
                        self.done = True
                    elif self.killable_clyde == True:
                        if self.clyde_previous_object == ".":
                            self.clyde_killed = True
                            self.clyde_moving = False
                            self.score += 10
                        elif self.clyde_previous_object == "o":
                            self.clyde_killed = True
                            self.clyde_moving = False
                            # setup killable
                            self.score += 100
                        elif self.clyde_previous_object == " ":
                            self.clyde_killed = True
                            self.clyde_moving = False
                            # setup killable
                else:
                    self.clyde_previous_object = self.board_ghost_check[self.clyde_state[0]][self.clyde_state[1]]
                    self.clyde_previous_state = copy(self.clyde_state)
                    self.clyde_state[1] = self.clyde_state[1] + 1
                    self.clyde_moving = True
        elif self.clyde_killed == True:
            pass

    def update_clyde_position(self, direction_clyde):
        if self.clyde_killed == False:
            if self.clyde_state == [10, 2] and direction_clyde == 3:
                self.board[self.clyde_previous_state[0]][self.clyde_previous_state[1]] = "["
                self.board[self.clyde_state[0]][self.clyde_state[1]] = "&"

            elif self.clyde_state == [10, 18] and direction_clyde == 2:
                self.board[self.clyde_previous_state[0]][self.clyde_previous_state[1]] = "]"
                self.board[self.clyde_state[0]][self.clyde_state[1]] = "&"

            elif self.clyde_moving == False:
                pass

            else:
                self.board[self.clyde_previous_state[0]][self.clyde_previous_state[1]] = self.clyde_previous_object
                self.board[self.clyde_state[0]][self.clyde_state[1]] = "&"
        elif self.clyde_killed == True:
            if self.board[self.clyde_state[0]][self.clyde_state[1]] != "&":
                pass
            elif self.board[self.clyde_state[0]][self.clyde_state[1]] == "&":
                self.board[self.clyde_state[0]][self.clyde_state[1]] = self.clyde_previous_object

    """
    ---------------------------------------------------------
    //MAP GENERATION
    ---------------------------------------------------------
    """

    def generate_map(self):
        for i in self.board:
            print(*i, sep=' ')

    def initialize_position(self):
        self.board[self.current_state[0]][self.current_state[1]] = "@"
        self.board[self.inky_state[0]][self.inky_state[1]] = "é"
        self.board[self.pinky_state[0]][self.pinky_state[1]] = "à"
        self.board[self.blinky_state[0]][self.blinky_state[1]] = "ç"
        self.board[self.clyde_state[0]][self.clyde_state[1]] = "&"


if __name__ == '__main__':
    """
    Il faut choisir un nombre entre 0 et 3
    - Si l'action est 0, déplacement vers le haut
    - Si l'action est 1, déplacement vers le bas
    - Si l'action est 2, déplacement vers la gauche
    - Si l'action est 3, déplacement vers la droite 
    
    @ : PacMan / é, ç, à, & : inky, blinky, pinky, clyde / #, |, - : murs / . : point / o : gros point 
    
    """

    world = Game()
    while world.done == False:
        print("-------------------------------------Next iteration-------------------------------------")
        world.step(random.randint(0, 3))

    print("-------------------------------------La partie est terminée-------------------------------------")
    print("--------------------------Votre score est de: {}".format(world.score))
    if world.score == 2500:
        reward = 1000
    elif world.score != 2500:
        reward = -300
