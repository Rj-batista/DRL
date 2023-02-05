class LineWorld:
    def __init__(self, nb_cells, start_cell, good_end_cell, bad_end_cell):
        self.done = None
        self.current_state = start_cell  # État actuel
        self.end_good_state = good_end_cell # État final
        self.end_bad_state = bad_end_cell
        self.num_states = nb_cells  # Nombre total d'états
        self.states = [i for i in range(nb_cells)]
        self.actions = [0, 1]
        self.num_actions = 2  # Nombre total d'actions possibles
        self.reward = 0  # Récompense actuelle
        self.line_world = ["_"] * (self.num_states - 1)
        self.line_world.insert(self.current_state,"X")
        
        
    def setState(self, st):
        self.current_state = st

    def isTerminateState(self):
        if (self.current_state == self.end_good_state) or (self.current_state == self.end_bad_state):
            return True
        else:
            return False
        
    def step(self, action):
        # Si l'action est 1, on avance à droite
        if (action == 1) and (self.isTerminateState() == False) :
            self.current_state += 1
            self.reward = 0  # Pas de récompense pour avancer
            self.line_world.remove("X")
            self.line_world.insert(self.current_state,"X")
            print(self.line_world)
        # Si l'action est 0, on avance à gauche
        elif (action == 0)and (self.isTerminateState() == False):
            self.current_state-= 1
            self.reward = 0  # Pas de récompense pour avancer
            self.line_world.remove("X")
            self.line_world.insert(self.current_state, "X")
            print(self.line_world)
        # Si l'on atteint l'état final, la partie est terminée
        if self.current_state == self.end_good_state:
            self.reward = 10  # Récompense de 1 pour atteindre l'état final
            #print(self.line_world)
            self.done = True
        elif self.current_state == self.end_bad_state:
            self.reward = -10
            #print(self.line_world)
            self.done = True
        return self.current_state, self.reward, self.done