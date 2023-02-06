import random

# Définir continue_or_stop
# Définir First_step (sauvegarde du player_board)
# Définir deuxième joueur

class Cant_stop:
    def __init__(self):
        self.game_boards = [[0] * 11] * 2
        self.general_board = [0] * 11
        self.player_board = [0] * 11
        self.done = False
        self.turn = 0   # 0 player / 1 computeur

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
                        break
                    self.game_boards[self.turn] = self.player_board.copy()
                    self.change_turn()
            else:
                print("No available moves")


    def roll_dices(self):
        self.combinations = []
        dices = [0, 0, 0, 0]
        for i in range(len(dices)):
            dices[i] = random.randint(1, 6)
        self.combinations.append((dices[0] + dices[1], dices[2] + dices[3]))
        self.combinations.append((dices[0] + dices[2], dices[1] + dices[3]))
        self.combinations.append((dices[0] + dices[3], dices[1] + dices[2]))
        print(self.combinations)
        print(dices)

    def available_moves(self):
        playable = []
        if self.bonze[1] == 0 and self.bonze[2] == 0:
            return self.remove_value_from_board(self.combinations)

        for c in self.combinations:

            if c[0] in self.bonze and c[1] in self.bonze:
                playable.append((c[0], c[1]))
                continue

            if self.bonze[-1] == 0:
                if c[0] == c[1]:
                    playable.append((c[0], c[1]))
                    continue

                if c[0] not in self.bonze and c[1] not in self.bonze:
                    playable.append(c[0])
                    playable.append(c[1])
                    continue
                else:
                    playable.append((c[0], c[1]))
                    continue

            if c[0] in self.bonze:
                playable.append(c[0])
                continue

            if c[1] in self.bonze:
                playable.append(c[1])
        return self.remove_value_from_board(playable)

    def remove_value_from_board(self, all_playable):
        clean_playable = []

        for i in range(len(all_playable)):
            if all_playable[i] == int and not self.general_board[all_playable[i]]:
                clean_playable.append(all_playable[i])

            elif all_playable[i] == tuple:
                if not self.general_board[all_playable[i][0]] and not self.general_board[all_playable[i][1]]:
                    clean_playable.append(all_playable[i])

                elif not self.general_board[all_playable[i][0]]:
                    clean_playable.append(all_playable[i][0])

                elif not self.general_board[all_playable[i][1]]:
                    clean_playable.append(all_playable[i][1])

        return clean_playable

    def move_bonze(self, chosen_action):
        if chosen_action == int:
            self.player_board[chosen_action - 2] += 1
        else:
            self.player_board[chosen_action[0] - 2] += 1
            self.player_board[chosen_action[1] - 2] += 1

    def move_to_play(self, action):
        print("Choose a move to play :")
        print(action)
        choice = input()
        self.move_bonze(action[choice])

    def change_board(self):
        limits = [3, 5, 7, 9, 11, 13, 11, 9, 7, 5, 3]
        for i in range(len(limits)):
            if self.player_board[i] >= limits[i]:
                self.general_board[i] = 1

    def is_game_over(self):
        if self.general_board.count(1) == 3 or self.general_board.count(2) == 3:
            self.done = True

    def continue_or_stop(self):
        choice = input("0: Continue / 1 : Stop")
        return bool(choice)

    def change_turn(self):
        self.turn = 1 if self.turn == 0 else 0
        self.first_step()


c = Cant_stop()
c.step()

# [7, 3, (5, 5), 4, 6]  coup double -> entre parenthèse / coup simple -> les autres