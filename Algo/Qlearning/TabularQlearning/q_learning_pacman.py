import math
import random
import itertools
import matplotlib.pyplot as plt
from tqdm import tqdm

import numpy as np
import numba
import numpy.random
from collections import deque

import tensorflow as tf
from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Embedding, Reshape
from tensorflow.keras.optimizers import Adam
import Env.Pac-Man.Pac-Man 
from Env.Pac-Man.Pac-Man import Game

def q_learning(env, max_iter_count = 10000, discount_factor=0.9):
    epsilon = 0.05
    alpha = 0.1
    max_steps_per_episode = 1000
    Q = {}
    reward_per_episode = []
    steps_per_episode = []
    
    for s in env.states:
        int_state = env.getStateInt(s)
        Q[int_state] = {0: 0, 1: 0, 2: 0, 3: 0}
            
    
    for episode in range(max_iter_count):
        print("Episode : ", episode)
        cumulative_reward = 0
        step = 0
        game_done = False
        
        while (game_done!=True):            
            current_Int_State = env.currentIntState
            actions = env.actions
            
            if np.random.uniform(0,1) <= epsilon:
                a = np.random.choice(actions)
            else:
                a = actions[np.argmax([Q[current_Int_State][a] for a in actions])]

            old_reward   = env.score
            env.step(a)
            print("\n-----------------------------------------------------\n")
            new_reward   = env.score
            diff_reward  = new_reward - old_reward

            n_Int_state = env.currentIntState
            n_actions = env.actions

            q_values_new_state = Q[n_Int_state]
            max_q_value = max(q_values_new_state.values())
            q_value_oldState = Q[current_Int_State][a]
            
            Q[current_Int_State][a] = q_value_oldState + alpha * (new_reward + (discount_factor*max_q_value) - q_value_oldState)
    
            cumulative_reward += new_reward
            step += 1
            
            if env.done == True:
                env.reset()
                game_done = True
                reward_per_episode.append(cumulative_reward)
                steps_per_episode.append(step)
            
            
        
    return reward_per_episode, steps_per_episode
            

if __name__ == '__main__':
    # Il faut choisir un nombre entre 0 et 3
    # Si l'action est 0, déplacement vers le haut
    # Si l'action est 1, déplacement vers le bas
    # Si l'action est 2, déplacement vers la gauche
    # Si l'action est 3, déplacement vers la droite
    world = Game()
    
    scores, steps = q_learning(world, max_iter_count = 1000, discount_factor=0.9)
    plt.plot(scores)
    plt.show()
    plt.plot(steps)
    plt.show()