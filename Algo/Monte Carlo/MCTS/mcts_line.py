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

def monte_carlo_tree_search_and_choose_action(env, iteration_count: int = 200) -> int:
    tree = {}

    root = env.current_state
    tree[root] = {}
    for a in env.actions:
        tree[root][a] = {
            'mean_score': 0.0,
            'selection_count': 0,
            'consideration_count': 0,
        }

    for _ in range(iteration_count):
        cloned_env = clone(env)
        current_node = cloned_env.current_state

        nodes_and_chosen_actions = []

        # SELECTION
        while not cloned_env.done and \
                not any(filter(lambda stats: stats['selection_count'] == 0, tree[current_node].values())):

            best_action = None
            best_action_score = None
            for (a, a_stats) in tree[current_node].items():
                ucb1_score = a_stats['mean_score'] + math.sqrt(2) * math.sqrt(
                    math.log(a_stats['consideration_count']) / a_stats['selection_count'])
                if best_action_score is None or ucb1_score > best_action_score:
                    best_action = a
                    best_action_score = ucb1_score

            nodes_and_chosen_actions.append((current_node, best_action))
            cloned_env.step(best_action)
            current_node = cloned_env.current_state

            if current_node not in tree:
                tree[current_node] = {}
                for a in cloned_env.actions:
                    tree[current_node][a] = {
                        'mean_score': 0.0,
                        'selection_count': 0,
                        'consideration_count': 0,
                    }

        # EXPAND
        if not cloned_env.done:
            random_action = np.random.choice(list(
                map(lambda action_and_stats: action_and_stats[0],
                    filter(lambda action_and_stats: action_and_stats[1]['selection_count'] == 0,
                           tree[current_node].items())
                    )
            ))

            nodes_and_chosen_actions.append((current_node, random_action))
            cloned_env.step(random_action)
            current_node = cloned_env.current_state

            if current_node not in tree:
                tree[current_node] = {}
                for a in cloned_env.actions:
                    tree[current_node][a] = {
                        'mean_score': 0.0,
                        'selection_count': 0,
                        'consideration_count': 0,
                    }

        # EVALUATE / ROLLOUT
        while not cloned_env.done:
            cloned_env.step(np.random.choice(cloned_env.actions))

        score = cloned_env.reward

        # BACKUP / BACKPROPAGATE / UPDATE STATS
        for (node, chose_action) in nodes_and_chosen_actions:
            for a in tree[node].keys():
                tree[node][a]['consideration_count'] += 1
            tree[node][chose_action]['mean_score'] = (
                    (tree[node][chose_action]['mean_score'] * tree[node][chose_action]['selection_count'] + score) /
                    (tree[node][chose_action]['selection_count'] + 1)
            )
            tree[node][chose_action]['selection_count'] += 1

    most_selected_action = None
    most_selected_action_selection_count = None

    for (a, a_stats) in tree[root].items():
        if most_selected_action_selection_count is None or a_stats[
            'selection_count'] > most_selected_action_selection_count:
            most_selected_action = a
            most_selected_action_selection_count = a_stats['selection_count']

    return most_selected_action
	
def run_n_games_and_return_mean_score(games_count: int) -> float:
    reward_per_episode = []
    env = LineWorld()
    total = 0.0
    wins = 0
    losses = 0
    draws = 0
    for _ in tqdm(range(games_count)):
        env.reset()

        while not env.done:
            chosen_a = monte_carlo_tree_search_and_choose_action(env)
            env.step(chosen_a)

        if env.reward > 0:
            wins += 1
        elif env.reward < 0:
            losses += 1
        else:
            draws += 1
        total += env.reward
        reward_per_episode.appen(env.reward)

    print(f"MCTS - wins : {wins}, losses : {losses}, draws : {draws}")
    print(f"MCTS - mean_score : {total / games_count}")
    return (total / games_count),reward_per_episode
	
if __name__ == "__main__":
    average, scores = run_n_games_and_return_mean_score(1000)
    plt.plot(scores)
    plt.show()