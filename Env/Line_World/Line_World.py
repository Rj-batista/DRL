class LineWorld:
    def __init__(self):
        self.done = None
        self.current_state = 3  # État actuel
        self.end_good_state = 5  # État final
        self.end_bad_state = 0
        self.num_states = 5  # Nombre total d'états
        self.states = [i for i in range(6)]
        self.actions = [0, 1]
        self.num_actions = 2  # Nombre total d'actions possibles
        self.reward = 0  # Récompense actuelle
        self.line_world = ["_"] * (self.num_states - 1)
        self.line_world.insert(self.current_state - 1, "X")
        self.P = {}
        self.initP()

    def setState(self, st):
        self.current_state = st

    def initP(self):
        for state in self.states:
            for action in self.actions:
                self.current_state = state
                state_, reward_, done_ = self.step(action)
                self.P[(state_, reward_, state, action)] = 1

    def isTerminateState(self):
        if (self.current_state == self.end_good_state) or (self.current_state == self.end_bad_state):
            return True
        else:
            return False

    def step(self, action):
        # Si l'action est 1, on avance à droite
        if (action == 1) and (self.isTerminateState() == False):
            self.current_state += 1
            self.reward = 0  # Pas de récompense pour avancer
            self.line_world.remove("X")
            self.line_world.insert(self.current_state - 1, "X")
            print(self.line_world)
        # Si l'action est 0, on avance à gauche
        elif (action == 0) and (self.isTerminateState() == False):
            self.current_state -= 1
            self.reward = 0  # Pas de récompense pour avancer
            self.line_world.remove("X")
            self.line_world.insert(self.current_state - 1, "X")
            print(self.line_world)
        # Si l'on atteint l'état final, la partie est terminée
        if self.current_state == self.end_good_state:
            self.reward = 1  # Récompense de 1 pour atteindre l'état final
            # print(self.line_world)
            self.done = True
        elif self.current_state == self.end_bad_state:
            self.reward = -3
            # print(self.line_world)
            self.done = True
        return self.current_state, self.reward, self.done