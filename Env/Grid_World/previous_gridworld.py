class GridWorld:
    def __init__(self):
        self.current_state = (0, 0)  # État actuel (ligne, colonne)
        self.end_state = (3, 3)  # État final (ligne, colonne)
        self.grid_size = (4, 4)  # Taille de la grille (lignes, colonnes)
        self.num_actions = 4  # Nombre total d'actions possibles (haut, bas, gauche, droite)
        self.reward = 0  # Récompense actuelle
        self.done = False  # Indique si la partie est terminée

    def step(self, action):
        # Si l'action est 0, on avance d'une ligne
        if action == 0:
            self.current_state = (self.current_state[0] - 1, self.current_state[1])
            self.reward = 0  # Pas de récompense pour avancer
        # Si l'action est 1, on recule d'une ligne
        elif action == 1:
            self.current_state = (self.current_state[0] + 1, self.current_state[1])
            self.reward = 0  # Pas de récompense pour avancer
        # Si l'action est 2, on avance d'une colonne
        elif action == 2:
            self.current_state = (self.current_state[0], self.current_state[1] - 1)
            self.reward = 0  # Pas de récompense pour avancer
        # Si l'action est 3, on recule d'une colonne
        elif action == 3:
            self.current_state = (self.current_state[0], self.current_state[1] + 1)
            self.reward = 0  # Pas de récompense pour avancer
        # Si l'on atteint l'état final, la partie est terminée
        if self.current_state == self.end_state:
            self.reward = 1  # Récompense de 1 pour atteindre l'état final
            self.done = True
        # Si l'on sort de la grille, on revient à l'état initial
        if self.current_state[0] < 0 or self.current_state[0] >= self.grid_size[0] or self.current_state[1] < 0 or \
                self.current_state[1] >= self.grid_size[1]:
            self.current_state = (0, 0)
            self.reward = -1  # Pénalité de -1 pour sortir de la grille
        return self.current_state, self.reward, self.done

world = GridWorld()
state, reward, done = world.step(0) # Avance