import math
import random
import itertools
import matplotlib.pyplot as plt

import numpy as np
import numba
import numpy.random
from Env.Line_World.line_world import LineWorld

def q_learning(line, max_iter_count = 10000, discount_factor=0.9):
    epsilon = 0.05
    alpha = 0.1
    max_steps_per_episode = 1000
    Q = {}
    reward_per_episode = []
    steps_per_episode = []
    line_nb_cells = line.num_states
    
    for s in line.states:
        Q[s] = {0: 0, 1: 0}
            
    
    for episode in range(max_iter_count):
        print("Episode : ", episode)
        cumulative_reward = 0
        step = 0
        game_done = False
        
        while (step<max_steps_per_episode) and (game_done!=True):            
            current_state = line.current_state
            actions = line.actions
            
            if np.random.uniform(0,1) <= epsilon:
                a = np.random.choice(actions)
            else:
                a = actions[np.argmax([Q[current_state][a] for a in actions])]

            old_reward   = line.reward
            line.step(a)
            new_reward   = line.reward

            n_state = line.current_state
            n_actions = line.actions

            print(n_state)
            q_values_new_state = Q[n_state]
            max_q_value = max(q_values_new_state.values())
            q_value_oldState = Q[current_state][a]
            
            Q[current_state][a] = q_value_oldState + alpha * (new_reward + (discount_factor*max_q_value) - q_value_oldState)
    
            cumulative_reward += new_reward
            step += 1
            
            if line.done == True:
                line.reset()
                game_done = True
            
            #print(cumulative_reward)
        reward_per_episode.append(cumulative_reward)
        steps_per_episode.append(step)
        
    return reward_per_episode, steps_per_episode
            

if __name__ == '__main__':
    world = LineWorld()
    scores, steps = q_learning(world, max_iter_count = 10000, discount_factor=0.9)
    print(scores)
    plt.plot(scores)
    plt.show()
    plt.plot(steps)
    plt.show()