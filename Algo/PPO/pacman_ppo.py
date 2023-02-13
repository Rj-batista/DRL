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
	
def model_prediction(pi_and_v_model: tf.keras.models.Model,
                     model_inputs):
    return pi_and_v_model(model_inputs)
	
def training_step(pi_and_v_model: tf.keras.models.Model,
                  model_inputs,
                  chosen_actions: int,
                  targets: float,
                  pi_old: np.ndarray,
                  deltas: float,
                  c1: float,
                  c2: float,
                  epochs: int,
                  opt):
    for _ in range(epochs):
        with tf.GradientTape() as tape:
            pi_s_pred, v_s_pred = pi_and_v_model(model_inputs)
            loss_vf = tf.reduce_mean((targets - tf.squeeze(v_s_pred)) ** 2)
            loss_entropy = - tf.reduce_sum(pi_s_pred * tf.math.log(pi_s_pred + 0.000000001))

            pi_s_a_pred = tf.gather(pi_s_pred, chosen_actions, batch_dims=1)
            pi_old_s_a_pred = tf.gather(pi_old, chosen_actions, batch_dims=1)

            r = pi_s_a_pred / (pi_old_s_a_pred + 0.0000000001)
            loss_policy_clipped = tf.reduce_sum(tf.minimum(r * deltas,
                                             tf.clip_by_value(r, 1.0 - 0.2, 1 + 0.2) * deltas))
            total_loss = -loss_policy_clipped + c1 * loss_vf - c2 * loss_entropy

        grads = tape.gradient(total_loss, pi_and_v_model.trainable_variables)
        opt.apply_gradients(zip(grads, pi_and_v_model.trainable_variables))
		
def ppo(env, max_iter_count: int = 10000,
        gamma: float = 0.99,
        learning_rate: float = 1e-5,
        actors_count: int = 10,
        epochs: int = 5,
        c1: float = 1.0,
        c2: float = 0.01):
    pi_and_v_input_state_desc = tf.keras.layers.Input((len(env.state_description()),))
    pi_and_v_input_mask = tf.keras.layers.Input((len(env.actions),))
    opt = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    hidden_tensor = pi_and_v_input_state_desc
    for _ in range(6):
        hidden_tensor = tf.keras.layers.Dense(128,
                                              activation=tf.keras.activations.tanh,
                                              use_bias=True
                                              )(hidden_tensor)

    output_pi_tensor = tf.keras.layers.Dense(len(env.actions),
                                             activation=tf.keras.activations.linear,
                                             use_bias=True
                                             )(hidden_tensor)

    output_v_tensor = tf.keras.layers.Dense(1,
                                            activation=tf.keras.activations.linear,
                                            use_bias=True
                                            )(hidden_tensor)

    output_pi_probs = tf.keras.layers.Softmax()(output_pi_tensor, pi_and_v_input_mask)

    pi_and_v_model = tf.keras.models.Model([pi_and_v_input_state_desc, pi_and_v_input_mask],
                                           [output_pi_probs, output_v_tensor])

    ema_score = 0.0
    first_episode = True

    ema_score_progress = []

    for _ in tqdm(range(max_iter_count)):

        envs = [clone(env) for _ in range(actors_count)]

        states = np.zeros((actors_count, len(env.state_description())))
        masks = np.zeros((actors_count, len(env.actions)))

        for i, env in enumerate(envs):
            if env.done:
                if first_episode:
                    ema_score = env.score
                    first_episode = False
                else:
                    ema_score = (1 - 0.999) * env.score + 0.999 * ema_score
                    ema_score_progress.append(ema_score)
                print(ema_score)
                env.reset()

            s = env.state_description()

            aa = env.actions

            mask = np.zeros((len(env.actions),))
            mask[aa] = 1.0

            states[i] = s
            masks[i] = mask

        pi_s_pred, v_s_pred = model_prediction(pi_and_v_model, [states, masks])

        chosen_actions = tf.squeeze(tf.random.categorical(tf.math.log(pi_s_pred), 1))

        rewards = np.zeros((actors_count,))
        states_p = np.zeros_like(states)
        masks_p = np.zeros_like(masks)
        game_overs = np.ones((actors_count,))
        for i, env in enumerate(envs):
            old_score = env.score
            print("action : ", chosen_actions[i])
            env.step(chosen_actions[i])
            new_score = env.score
            r = new_score - old_score

            rewards[i] = r

            s_p = env.state_description()
            aa_p = env.actions

            mask_p = np.zeros((len(env.actions),))

            if len(aa_p) > 0:
                mask_p[aa_p] = 1.0

            states_p[i] = s_p
            masks_p[i] = mask_p

            if env.done:
                game_overs[i] = 0.0

        ### TRAINING TIME !!!

        pi_s_p_pred, v_s_p_pred = model_prediction(pi_and_v_model, [states_p, masks_p])

        targets = tf.constant(rewards + gamma * tf.squeeze(v_s_p_pred) * game_overs)

        deltas = targets - tf.constant(tf.squeeze(v_s_pred))  # for now it's At = Advantage of playing action a
        pi_old = tf.constant(pi_s_pred)

        training_step(pi_and_v_model, [states, masks], chosen_actions, targets, pi_old, deltas, c1, c2, epochs, opt)

    return pi_and_v_model, ema_score_progress
	
pi_and_v_model, scores = ppo(Game(), max_iter_count=1000)
print(pi_and_v_model.weights)
plt.plot(scores)
plt.show()