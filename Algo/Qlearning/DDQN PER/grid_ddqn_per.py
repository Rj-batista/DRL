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
	
	
def ddqn_per(env, episodes=1000, gamma=0.99, alpha=0.1, epsilon=0.1):
    q_network = build_compile_model(env)
    target_network = build_compile_model(env)
    nb_steps = 0
    first_episode = True
    
    step = 0
    reward = 0
    cumumated_reward = 0
    reward_per_episode = []
    step_by_episode = []
    batch_size = 32
    memory = deque(maxlen=2000)
    priority = deque(maxlen=2000)
    
    for iteration in range(episodes):
        print("Episode : ", iteration)
        
        while not env.done:
            
            actions = env.actions
            current_state = env.currentIntState
            q_values = q_network.predict(np.array([current_state]))[0]
            if np.random.rand() < epsilon:
                a = np.random.choice(actions)
            else:
                a= np.argmax(q_values)

            old_reward = env.reward
            env.step(a)
            new_state = env.currentIntState
            reward = env.reward
            done = env.done
            print(reward)
            memory.append((old_reward, a, reward, new_state, done))
            priority.append(abs(reward + gamma * np.amax(target_network.predict(np.array([new_state]))[0]) - q_values[a]))

            if (len(memory) > batch_size):
                priority_sum = np.sum(priority)
                probabilities = [p/priority_sum for p in priority]
                minibatch = np.random.choice(len(memory), batch_size, p=probabilities, replace=False)
                for m in minibatch:
                    s, ac, rreward, ns, terminated = memory[m]
                    q_values = q_network.predict(np.array([s]))[0]
                    if terminated:
                        q_values[a] = rreward
                    else:
                        t = target_network.predict(np.array([ns]))[0]
                        q_values[a] = rreward + gamma * np.amax(t)
                    q_network.fit(np.array([s]), np.array([q_values]), verbose=0)

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
	
world = GridWorld()
#For 1000
scores, steps = ddqn_per(world, episodes = 1000)
plt.plot(scores)
plt.show()
plt.plot(steps)
plt.show()