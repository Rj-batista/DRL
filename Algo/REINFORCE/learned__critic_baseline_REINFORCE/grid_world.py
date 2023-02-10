import matplotlib.pyplot as plt
import numpy as np
import numpy.random
import tensorflow as tf
from tqdm import tqdm
from Env.Grid_World.grid_world import GridWorld


def REINFORCE_with_learned_baseline(env: GridWorld, max_iter_count: int = 10000,
                                    gamma: float = 0.99,
                                    alpha_pi: float = 0.01,
                                    alpha_v: float = 0.01):
    pi = tf.keras.models.Sequential()
    pi.add(tf.keras.layers.Dense(env.num_actions,
                                 activation=tf.keras.activations.softmax,
                                 use_bias=True
                                 ))

    v = tf.keras.models.Sequential()
    v.add(tf.keras.layers.Dense(1,
                                activation=tf.keras.activations.linear,
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

    for _ in tqdm(range(max_iter_count)):
        if env.done:
            ### TRAINING TIME !!!
            G = 0.0

            for t in reversed(range(0, len(episode_states_buffer))):
                G = episode_rewards_buffer[t] + gamma * G

                with tf.GradientTape() as tape_v:
                    v_s_pred = v(np.array([episode_states_buffer[t]]))[0][0]

                delta = G - tf.constant(v_s_pred)

                grad_v_s_pred = tape_v.gradient(v_s_pred, v.trainable_variables)
                for (var, grad) in zip(v.trainable_variables, grad_v_s_pred):
                    if grad is not None:
                        var.assign_add(alpha_v * delta * grad)

                with tf.GradientTape() as tape_pi:
                    pi_s_a_t = pi(np.array([episode_states_buffer[t]]))[0][episode_actions_buffer[t]]
                    log_pi_s_a_t = tf.math.log(pi_s_a_t)

                grads = tape_pi.gradient(log_pi_s_a_t, pi.trainable_variables)

                for (var, grad) in zip(pi.trainable_variables, grads):
                    if grad is not None:
                        var.assign_add(alpha_pi * (gamma ** t) * delta * grad)

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

        s = np.array([env.currentIntState])

        episode_states_buffer.append(s)

        aa = env.actions

        pi_s = pi(np.array([s]))[0].numpy()
        allowed_pi_s = pi_s[aa]
        sum_allowed_pi_s = np.sum(allowed_pi_s)
        if sum_allowed_pi_s == 0.0 or np.isnan(sum_allowed_pi_s):
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
    return pi, v, ema_score_progress, ema_nb_steps_progress


game = GridWorld(taille=[6, 6], position_start=[0, 1], good_end_position=[4, 2], bad_end_position=[3, 5])
pi, v, scores, steps = REINFORCE_with_learned_baseline(game, max_iter_count=10000)
print(pi.weights)
print(scores)
