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

def clone(env):
    new_env = Game()
    new_env.currentIntState = env.currentIntState
    new_env.current_state = env.current_state.copy()
    new_env.previous_state = env.previous_state.copy()
    new_env.inky_state = env.inky_state.copy()
    new_env.inky_previous_object = env.inky_previous_object
    new_env.killable_inky = env.killable_inky
    new_env.inky_killed = env.inky_killed
    
    new_env.blinky_state = env.blinky_state.copy()
    new_env.blinky_previous_object = env.blinky_previous_object
    new_env.killable_blinky = env.killable_blinky
    new_env.blinky_killed = env.blinky_killed
    
    new_env.pinky_state = env.pinky_state.copy()
    new_env.pinky_previous_object = env.pinky_previous_object
    new_env.killable_pinky = env.killable_pinky
    new_env.pinky_killed = env.pinky_killed
    
    
    new_env.clyde_state = env.clyde_state
    new_env.clyde_previous_object = env.clyde_previous_object
    new_env.killable_clyde = env.killable_clyde
    new_env.clyde_killed = env.clyde_killed
    new_env.currentIntState = env.currentIntState
    
    new_env.score = env.score 
    new_env.done = env.done  # Indique si la partie est terminée
    new_env.compteur_first_step = env.compteur_first_step
    new_env.compteur_ghost = env.compteur_ghost
    new_env.fruit_collision = env.fruit_collision
    #new_env.initialize_position()
    new_env.board = env.board
    new_env.board_ghost_check = env.board_ghost_check
    new_env.generate_map()
    
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

            action_score += cloned_env.score
        average_action_score = action_score / simulation_count_per_action

        if best_action_average_score is None or best_action_average_score < average_action_score:
            best_action = a
            best_action_average_score = average_action_score
    return best_action


def run_ttt_n_games_and_return_mean_score(games_count: int) -> float:
    rewards_per_episode = []
    steps_per_episode = []
    env = Game()
    total = 0.0
    step = 0
    for _ in tqdm(range(games_count)):
        step = 0
        env.reset()

        while not env.done:
            chosen_a = monte_carlo_random_rollout_and_choose_action(env)
            env.step(chosen_a)
            step += 1

        rewards_per_episode.append(env.score)
        steps_per_episode.append(step)
        total += env.score
    return (total / games_count), rewards_per_episode, steps_per_episode
	
if __name__ == "__main__":
    average, scores, steps = run_ttt_n_games_and_return_mean_score(1000)