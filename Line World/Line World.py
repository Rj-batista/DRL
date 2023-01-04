class LineWorld:
    def __init__(self):
        self.done = None
        self.current_state = 3  # État actuel
        self.end_good_state = 5 # État final
        self.end_bad_state = 0
        self.num_states = 5  # Nombre total d'états
        self.num_actions = 2  # Nombre total d'actions possibles
        self.reward = 0  # Récompense actuelle
        self.line_world = ["_"] * self.num_states
        self.line_world.insert(self.current_state-1,"X")

    def step(self, action):
        # Si l'action est 0, on avance à droite
        if action == 1:
            self.current_state += 1
            self.reward = 0  # Pas de récompense pour avancer
            self.line_world.remove("X")
            self.line_world.insert(self.current_state-1,"X")
            print(self.line_world)
        # Si l'action est 1, on avance à gauche
        elif action == 0:
            self.current_state-= 1
            self.reward = 0  # Pas de récompense pour avancer
            self.line_world.remove("X")
            self.line_world.insert(self.current_state - 1, "X")
            print(self.line_world)
        # Si l'on atteint l'état final, la partie est terminée
        if self.current_state == self.end_good_state:
            self.reward = 1  # Récompense de 1 pour atteindre l'état final
            print(self.line_world)
            self.done = True
        elif self.current_state == self.end_bad_state:
            self.reward = -3
            print(self.line_world)
            self.done = True
        return self.current_state, self.reward, self.done


if __name__ == '__main__':
    world = LineWorld()
    state, reward, done = world.step(0) # Avance d'un état