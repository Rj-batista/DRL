import random
import tensorflow as tf

# Définir continue_or_stop
# Définir First_step (sauvegarde du player_board)
# Définir deuxième joueur

class Cant_stop:
    def __init__(self):
        self.game_boards = [[0] * 11] * 2
        self.general_board = [0] * 11
        self.player_board = [0] * 11
        self.done = False
        self.turn = 0  # 0 player / 1 computeur
        self.bonze = [0, 0, 0]
        self.reward = 0

    def first_step(self):
        self.bonze = [0, 0, 0]
        self.player_board = self.game_boards[self.turn].copy()
        self.step()

    def step(self):
        continue_playing = True
        while continue_playing:
            self.roll_dices()
            actions = self.available_moves()
            if actions:
                self.move_to_play(actions)
                self.change_board()
                continue_playing = self.continue_or_stop()
                if not continue_playing:
                    self.is_game_over()
                    if self.done:
                        self.game_over()
                        return
                    self.game_boards[self.turn] = self.player_board.copy()
            else:
                continue_playing = False
                print("No available moves")
        if not self.turn:
            print("L'ordinateur a joué son tour.")
        self.change_turn()

    def roll_dices(self):
        self.combinations = []
        dices = [0, 0, 0, 0]
        for i in range(len(dices)):
            dices[i] = random.randint(1, 6)
        self.combinations.append((dices[0] + dices[1], dices[2] + dices[3]))
        self.combinations.append((dices[0] + dices[2], dices[1] + dices[3]))
        self.combinations.append((dices[0] + dices[3], dices[1] + dices[2]))

    def available_moves(self):
        playable = []
        if self.bonze[1] == 0 and self.bonze[2] == 0:
            return self.remove_value_from_board(self.combinations)

        for combi in self.combinations:
            if combi[0] in self.bonze and combi[1] in self.bonze:
                playable.append((combi[0], combi[1]))
                continue

            if self.bonze[-1] == 0:
                if combi[0] == combi[1]:
                    playable.append((combi[0], combi[1]))
                    continue

                if combi[0] not in self.bonze and combi[1] not in self.bonze:
                    playable.append(combi[0])
                    playable.append(combi[1])
                    continue
                else:
                    playable.append((combi[0], combi[1]))
                    continue

            if combi[0] in self.bonze:
                playable.append(combi[0])
                continue

            if combi[1] in self.bonze:
                playable.append(combi[1])
        return self.remove_value_from_board(playable)

    def remove_value_from_board(self, all_playable):
        clean_playable = []

        for i in range(len(all_playable)):
            if isinstance(all_playable[i], int) and not self.general_board[all_playable[i] - 2]:
                clean_playable.append(all_playable[i])

            elif isinstance(all_playable[i], tuple):
                if not self.general_board[all_playable[i][0] - 2] and not self.general_board[all_playable[i][1] - 2]:
                    clean_playable.append(tuple(sorted(all_playable[i])))

                elif not self.general_board[all_playable[i][0] - 2]:
                    clean_playable.append(all_playable[i][0])

                elif not self.general_board[all_playable[i][1] - 2]:
                    clean_playable.append(all_playable[i][1])

        return clean_playable

    def update_bonze(self, chosen_action):
        if isinstance(chosen_action, tuple):
            if chosen_action[0] in self.bonze:
                chosen_action = chosen_action[1]
            elif chosen_action[1] in self.bonze:
                chosen_action = chosen_action[0]
            elif chosen_action[0] == chosen_action[1]:
                chosen_action = chosen_action[0]
            else:
                for i in range(len(self.bonze) - 1):
                    if self.bonze[i] == 0:
                        self.bonze[i] = chosen_action[0]
                        self.bonze[i + 1] = chosen_action[1]
                        return
        if chosen_action in self.bonze:
            return
        for i in range(len(self.bonze)):
            if self.bonze[i] == 0:
                self.bonze[i] = chosen_action
                return

    def move_bonze(self, chosen_action):
        self.update_bonze(chosen_action)
        if isinstance(chosen_action, int):
            self.player_board[chosen_action - 2] += 1
        else:
            self.player_board[chosen_action[0] - 2] += 1
            self.player_board[chosen_action[1] - 2] += 1

    def move_to_play(self, action):
        if self.turn:
            self.move_bonze(action[random.randint(0, len(action) - 1)])
            return
        self.view()
        print("Choisissez sur quelle(s) colonne(s) vous voulez avancer :")
        action = list(set(action))
        for i in range(len(action)):
            print(i, ' : ', action[i])
        choice = input()
        self.move_bonze(action[int(choice)])

    def change_board(self):
        limits = [3, 5, 7, 9, 11, 13, 11, 9, 7, 5, 3]
        for i in range(len(limits)):
            if self.player_board[i] >= limits[i]:
                self.general_board[i] = self.turn + 1
                self.player_board[i] = limits[i]

    def is_game_over(self):
        if self.general_board.count(1) == 3 or self.general_board.count(2) == 3:
            self.done = True

    def game_over(self):
        if self.turn:
            print("L'avancée du robot : ", self.player_board)
            print("L'ordinateur a gagné la partie.")
        else:
            print("Bravo ! Vous avez gagné la partie !!")

    def continue_or_stop(self):
        if self.turn:
            return bool(random.randint(0, 1))
        self.view()
        choice = input("0: S'arrêter / 1 : Continuer :\n")
        return bool(int(choice))

    def change_turn(self):
        self.turn = 1 if self.turn == 0 else 0
        self.first_step()

    def view(self):
        print("Votre avancée : ", self.player_board)
        print("L'avancée du robot : ", self.game_boards[1])
        print("Position de vos bonzes : ", self.bonze)

    def state_id(self):
        pass

    def state_description(self):
        return tf.keras.utils.to_categorical([] * 83, 3).flatten

    def state_dim(self):
        return 249 # 83*3

    def reset(self):
        self.game_boards = [[0] * 11] * 2
        self.general_board = [0] * 11
        self.player_board = [0] * 11
        self.done = False
        self.turn = 0  # 0 player / 1 computeur
        self.bonze = [0, 0, 0]
        self.reward = 0

    def clone(self):
        new_env = Cant_stop()
        new_env.game_boards = self.game_boards.copy()
        new_env.general_board = self.general_board.copy()
        new_env.player_board = self.player_board.copy()
        new_env.turn = self.turn
        new_env.bonze = self.bonze.copy()
        new_env.reward = self.reward
        return new_env

    def max_actions_count(self):
        return 77

    def available_actions_ids(self):
        pass

c = Cant_stop()
c.first_step()
