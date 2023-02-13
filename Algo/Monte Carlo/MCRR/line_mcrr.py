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

def clone(env):
    new_env = LineWorld()
    new_env.current_state = env.current_state
    new_env.num_states = env.num_states
    new_env.actions = env.actions.copy()
    new_env.done = env.done
    new_env.reward = env.reward
    return new_env

def monte_carlo_random_rollout_and_choose_action(env,simulation_count_per_action: int = 50) -> int:
    best_action = None
    best_action_average_score = None
    for a in np.array(env.actions):
        action_score = 0.0
        for _ in range(simulation_count_per_action):
            cloned_env = clone(env)
            cloned_env.step(a)

            while not cloned_env.done:
                cloned_env.step(np.random.choice(np.array(cloned_env.actions)))

            action_score += cloned_env.reward
        average_action_score = action_score / simulation_count_per_action

        if best_action_average_score is None or best_action_average_score < average_action_score:
            best_action = a
            best_action_average_score = average_action_score
    return best_action


def run_ttt_n_games_and_return_mean_score(games_count: int) -> float:
    rewards_per_episode = []
    steps_per_episode = []
    env = LineWorld()
    total = 0.0
    step = 0
    for _ in tqdm(range(games_count)):
        env.reset()

        while not env.done:
            chosen_a = monte_carlo_random_rollout_and_choose_action(env)
            env.step(chosen_a)
            step += 1

        rewards_per_episode.append(env.reward)
        steps_per_episode.append(step)
        total += env.reward
    return (total / games_count), rewards_per_episode, rewards_per_episode
	
if __name__ == "__main__":
    average, scores, steps = run_ttt_n_games_and_return_mean_score(1000)