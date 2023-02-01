class GridWorld:
    def __init__(self, taille, position_start, good_end_position, bad_end_position):
        self.current_state = position_start  # État actuel (ligne, colonne)
        self.states = [[x, y] for x in range(taille[0]) for y in range(taille[1])]
        self.end_good_state = good_end_position  # État final (ligne, colonne)
        self.end_bad_state = bad_end_position
        self.grid_size = taille  # Taille de la grille (lignes, colonnes)
        self.stateSpace = {}
        self.matchStates()
        self.num_actions = 4  # Nombre total d'actions possibles (haut, bas, gauche, droite)
        self.reward = 0  # Récompense actuelle
        self.done = False  # Indique si la partie est terminée
        self.generate_grid()
        self.actions = [2, 3, 0, 1]
        self.rewards = [0, 1, 3]
        self.actionSpace = {0: -self.grid_size[0], 1: self.grid_size[0],
                            2: -1, 3: 1}
        self.P = {}
        self.initP()

    def matchStates(self):
        i = 0
        for s in self.states:
            self.stateSpace[str(s)] = i
            i = i + 1

    def getStateInt(self, st):
        return self.stateSpace[str(st)]

    def getStateCouple(self, st):
        n_state = {i for i in self.stateSpace if self.stateSpace[i] == st}
        return list(n_state)

    def initP(self):
        for state in self.states:
            st = self.getStateInt(state)
            for action in self.actions:
                self.current_state = state
                state_, reward_, done_ = self.step(action)
                stt = self.getStateInt(state_)
                self.P[(stt, reward_, st, action)] = 1

    def step(self, action):
        if action == 0:
            if self.current_state[0] == 0:
                self.current_state[0] = self.grid_size[0] - 1
                self.reward = 0  # Pas de récompense pour traverser le mur
                self.generate_grid()
                self.endgame()
            else:
                self.current_state[0] = self.current_state[0] - 1
                self.reward = 0  # Pas de récompense pour avancer
                self.generate_grid()
                self.endgame()

        elif action == 1:
            if self.current_state[0] == self.grid_size[0] - 1:
                self.current_state[0] = 0
                self.reward = 0  # Pas de récompense pour avancer
                self.generate_grid()
                self.endgame()
            else:
                self.current_state[0] = self.current_state[0] + 1
                self.reward = 0  # Pas de récompense pour avancer
                self.generate_grid()
                self.endgame()

        elif action == 2:
            if self.current_state[1] == 0:
                self.current_state[1] = self.grid_size[1] - 1
                self.reward = 0  # Pas de récompense pour avancer
                self.generate_grid()
                self.endgame()
            else:
                self.current_state[1] = self.current_state[1] - 1
                self.reward = 0  # Pas de récompense pour avancer
                self.generate_grid()
                self.endgame()

        elif action == 3:
            if self.current_state[1] == self.grid_size[1] - 1:
                self.current_state[1] = 0
                # print(self.current_state)
                self.reward = 0  # Pas de récompense pour avancer
                self.generate_grid()
                self.endgame()
            else:
                self.current_state[1] = self.current_state[1] + 1
                self.reward = 0  # Pas de récompense pour avancer
                self.generate_grid()
                self.endgame()
                # Si l'on atteint l'état final, la partie est terminée
        return self.current_state, self.reward, self.done

    def endgame(self):
        if self.current_state == self.end_good_state:
            self.reward = 1  # Récompense de 1 pour atteindre l'état final
            self.done = True
        elif self.current_state == self.end_bad_state:
            self.reward = 3
            self.done = True

    # def update_grid(self):
    #     new_grid = [["_", "_", "_", "_"],
    #                 ["_", "_", "_", "_"],
    #                 ["_", "_", "_", "_"],
    #                 ["_", "_", "_", "_"]]
    #     new_grid[self.current_state[0]][self.current_state[1]] = "X"
    #     for i in new_grid:
    #         print(i)

    def generate_grid(self):
        grid = []
        for i in range(self.grid_size[0]):
            grid.append([])
            for j in range(self.grid_size[1]):
                grid[i].append("_")
        grid[self.current_state[0]][self.current_state[1]] = "X"


"""        for i in grid:
            print(i)
        print("\n")"""