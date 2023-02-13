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
from Env.Line_World.line_world import LineWorld

def build_compile_model(line):
    model = tf.keras.models.Sequential()
    model.add(Dense(24, input_dim=1, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(len(line.actions), activation='linear'))

    model.compile(loss='mse', optimizer=Adam(learning_rate=0.01))
    return model
	
def ddqn(env, max_iter=1000, gamma=0.99, alpha=0.1, epsilon=0.1):
    q_network = build_compile_model(env)
    target_network = build_compile_model(env)
    nb_steps = 0
    first_episode = True
    
    cumumated_reward = 0
    step = 0
    reward = 0
    reward_per_episode = []
    step_by_episode = []
    batch_size = 32
    memory = deque(maxlen=2000)
    
    for iteretion in range(max_iter):
        print("Iteration : ", iteretion)
        
        while not env.done:
            actions = env.actions
            current_state = env.current_state
            q_values = q_network.predict(np.array([current_state]))[0]
            if np.random.rand() < epsilon:
                a = np.random.choice(actions)
            else:
                a= np.argmax(q_values)

            old_reward = env.reward
            env.step(a)
            new_state = env.current_state
            reward = env.reward
            done = env.done
            memory.append((old_reward, a, reward, new_state, done))

            if done:
                    q_values[a] = reward
            else:
                t = target_network.predict(np.array([new_state]))[0]
                q_values[a] = reward + gamma * np.amax(t)
            q_network.fit(np.array([current_state]), np.array([q_values]), verbose=0)

            cumumated_reward += reward
            step += 1

            if done:
                target_network.set_weights(q_network.get_weights())
        
        reward_per_episode.append(env.reward)
        step_by_episode.append(step)
        env.reset()
        step = 0
        cumumated_reward = 0
                
    return reward_per_episode, step_by_episode
	
world = LineWorld()
#For 1000
scores, steps = ddqn(world, max_iter = 1000)
plt.plot(scores)
plt.show()
plt.plot(steps)
plt.show()