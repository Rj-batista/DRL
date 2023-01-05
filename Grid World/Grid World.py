class GridWorld:
    def __init__(self, taille, position_start, good_end_position, bad_end_position):
        self.current_state = position_start  # État actuel (ligne, colonne)
        self.end_good_state = good_end_position  # État final (ligne, colonne)
        self.end_bad_state = bad_end_position
        self.grid_size = taille  # Taille de la grille (lignes, colonnes)
        self.num_actions = 4  # Nombre total d'actions possibles (haut, bas, gauche, droite)
        self.reward = 0  # Récompense actuelle
        self.done = False  # Indique si la partie est terminée
        self.generate_grid()

    def step(self, action):
        if action == 0:
            if self.current_state[0] == 0 :
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
            else :
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
                print(self.current_state)
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
        grid=[]
        for i in range(self.grid_size[0]):
            grid.append([])
            for j in range(self.grid_size[1]):
                grid[i].append("_")
        grid[self.current_state[0]][self.current_state[1]] = "X"
        for i in grid:
            print(i)

if __name__ == '__main__':
    # Il faut choisir un nombre entre 0 et 3
    # Si l'action est 0, déplacement vers le haut
    # Si l'action est 1, déplacement vers le bas
    # Si l'action est 2, déplacement vers la gauche
    # Si l'action est 3, déplacement vers la droite
    world = GridWorld([5,6],[0,5],[4,0],[3,2]) #taille, position de départ, fin de jeu reward positive, fin de jeu reward négative
    print(                                       )
    state, reward, done = world.step(0)


