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

def REINFORCE_with_mean_baseline(env, max_iter_count: int = 10000,
                                  gamma: float = 0.99,
                                  alpha_pi: float = 0.01,
                                  alpha_v: float = 0.01):
    pi = tf.keras.models.Sequential()
    pi.add(tf.keras.layers.Dense(len(env.actions),
                                 activation=tf.keras.activations.softmax,
                                 use_bias=True
                                 ))


    ema_score = 0.0
    ema_nb_steps = 0.0
    first_episode = True

    step = 0
    ema_score_progress = []
    ema_nb_steps_progress = []

    episode_states_buffer = []
    episode_actions_buffer = []
    episode_rewards_buffer = []
    
    mean_baseline = 0.0

    for _ in tqdm(range(max_iter_count)):
        print("New Episode ")
            ### TRAINING TIME !!!
            
        while not env.done:
            s = env.state_description()

            episode_states_buffer.append(s)

            aa = env.actions

            pi_s = pi(np.array([s]))[0].numpy()
            allowed_pi_s = pi_s[aa]
            sum_allowed_pi_s = np.sum(allowed_pi_s)
            if sum_allowed_pi_s == 0.0:
                probs = np.ones((len(aa),)) * 1.0 / (len(aa))
            else:
                probs = allowed_pi_s / sum_allowed_pi_s

            a = np.random.choice(aa, p=probs)

            episode_actions_buffer.append(a)

            old_score = env.reward
            env.step(a)
            new_score = env.reward
            r = new_score - old_score

            episode_rewards_buffer.append(r)

            step += 1
        
        G = 0.0

        for t in reversed(range(0, len(episode_states_buffer))):
            G = episode_rewards_buffer[t] + gamma * G

            delta = G - mean_baseline
                

            with tf.GradientTape() as tape_pi:
                pi_s_a_t = pi(np.array([episode_states_buffer[t]]))[0][episode_actions_buffer[t]]
                log_pi_s_a_t = tf.math.log(pi_s_a_t)

            grads = tape_pi.gradient(log_pi_s_a_t, pi.trainable_variables)

            for (var, grad) in zip(pi.trainable_variables, grads):
                if grad is not None:
                    var.assign_add(alpha_pi * (gamma ** t) * delta * grad)

        mean_baseline = ((mean_baseline * step) + G) / (step + 1)
            
        if first_episode:
            ema_score = env.reward
            ema_nb_steps = step
            first_episode = False
        else:
            ema_score = (1 - 0.95) * env.reward + 0.95 * ema_score
            ema_nb_steps = (1 - 0.95) * step + 0.95 * ema_nb_steps
            ema_score_progress.append(ema_score)
            ema_nb_steps_progress.append(ema_nb_steps)

        env.reset()
        episode_states_buffer.clear()
        episode_actions_buffer.clear()
        episode_rewards_buffer.clear()
        step = 0

    return pi, mean_baseline, ema_score_progress, ema_nb_steps_progress

if __name__ == '__main__':
    world = GridWorld()
    pi, v, scores, steps = REINFORCE_with_mean_baseline(world)
    print(pi.weights)
    plt.plot(scores)
    plt.show()
    plt.plot(steps)
    plt.show()