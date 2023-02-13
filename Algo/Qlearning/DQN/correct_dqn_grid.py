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
from Env.Grid_World.grid_world import GridWorld


def build_compile_model(env):
    model = tf.keras.models.Sequential()
    model.add(Dense(24, input_dim=1, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(len(env.actions), activation='linear'))

    model.compile(loss='mse', optimizer=Adam(learning_rate=0.01))
    return model
	
def dqn(env, max_iter=1000, gamma=0.99, alpha=0.1, epsilon=0.1):
    q_network = build_compile_model(env)
    nb_steps = 0
    first_episode = True
    
    step = 0
    reward = 0
    reward_per_episode = []
    step_by_episode = []
    
    for iteration in range(max_iter):
        print("Episode : ",iteration)
        while not env.done:
            actions = env.actions
            current_state = env.currentIntState
            q_values = q_network.predict(np.array([current_state]))[0]
            if np.random.rand() < epsilon:
                a = np.random.choice(actions)
            else:
                a= np.argmax(q_values)

            old_reward = env.reward
            print("old reward : ", old_reward)
            print("action : ", a)
            env.step(a)
            new_state = env.currentIntState
            reward = env.reward
            print("New reward : ", reward)
            done = env.done

            q_values[a] = reward + gamma * np.amax(q_network.predict(np.array([new_state]))[0])
            q_network.fit(np.array([current_state]), np.array([q_values]), verbose=0)
            current_state = new_state

            step += 1

            
        if env.done:
            print("Game Over")
            reward_per_episode.append(env.reward)
            step_by_episode.append(step)
            env.reset()
            step = 0
            cumumated_reward = 0
    return reward_per_episode, step_by_episode
    q_network = build_compile_model(env)
    nb_steps = 0
    first_episode = True
    
    step = 0
    reward = 0
    reward_per_episode = []
    step_by_episode = []
    
    for iteration in range(max_iter):
        print(iteration)
        if env.done:
            reward_per_episode.append(env.reward)
            step_by_episode.append(step)
            env.reset()
            step = 0
            cumumated_reward = 0
            
        actions = env.actions
        current_state = env.currentIntState
        q_values = q_network.predict(np.array([current_state]))[0]
        if np.random.rand() < epsilon:
            a = np.random.choice(actions)
        else:
            a= np.argmax(q_values)

        old_reward = env.reward
        new_state, reward, done = env.step(a)
        print(done)

        q_values[a] = reward + gamma * np.amax(q_network.predict(np.array([new_state]))[0])
        q_network.fit(np.array([current_state]), np.array([q_values]), verbose=0)
        current_state = new_state
            
        step += 1

    return reward_per_episode, step_by_episode
	
if __name__ == '__main__':
    world = GridWorld()
    #For 1000
    scores, steps = dqn(world, max_iter = 1000)
    plt.plot(scores)
    plt.show()
    plt.plot(steps)
    plt.show()
    
    #For 10000
    scores, steps = dqn(world, max_iter = 10000)
    plt.plot(scores)
    plt.show()
    plt.plot(steps)
    plt.show()