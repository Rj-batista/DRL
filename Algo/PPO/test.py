import math
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import matplotlib.pyplot as plt
import numpy as np
import numpy.random
import tensorflow as tf
from tqdm import tqdm


class DeepSingleAgentEnv:
    def max_action_count(self) -> int:
        pass

    def state_description(self) -> np.ndarray:
        pass

    def state_dim(self) -> int:
        pass

    def is_game_over(self) -> bool:
        pass

    def act_with_action_id(self, action_id: int):
        pass

    def score(self) -> float:
        pass

    def available_actions_ids(self) -> np.ndarray:
        pass

    def reset(self):
        pass

    def view(self):
        pass

    def clone(self) -> 'DeepSingleAgentEnv':
        pass


@tf.function
def model_prediction(pi_and_v_model: tf.keras.models.Model,
                     model_inputs):
    return pi_and_v_model(model_inputs)


@tf.function
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


class TTTVsRandom(DeepSingleAgentEnv):
    def __init__(self):
        self.grid = np.zeros((3, 3))
        self.game_over = False
        self.aa = [i for i in range(9)]
        self.current_score = 0.0

    def state_description(self) -> np.ndarray:
        return tf.keras.utils.to_categorical(self.grid, 3).flatten()

    def state_dim(self) -> int:
        return 27

    def max_action_count(self) -> int:
        return 9

    def is_game_over(self) -> bool:
        return self.game_over

    def act_with_action_id(self, action_id: int):
        assert (not self.is_game_over())
        row = action_id // 3
        col = action_id % 3
        assert (self.grid[row, col] == 0)

        self.grid[row, col] = 1
        self.aa.remove(action_id)

        if self.grid[row, 0] == self.grid[row, 1] and self.grid[row, 0] == self.grid[row, 2] or \
                self.grid[0, col] == self.grid[1, col] and self.grid[0, col] == self.grid[2, col] or \
                self.grid[1, 1] == self.grid[0, 0] and self.grid[1, 1] == self.grid[2, 2] and self.grid[1, 1] == 1 or \
                self.grid[2, 0] == self.grid[1, 1] and self.grid[0, 2] == self.grid[1, 1] and self.grid[1, 1] == 1:
            self.current_score = 1.0
            self.game_over = True
            return

        if len(self.aa) == 0:
            self.current_score = 0.0
            self.game_over = True
            return

        action_id = np.random.choice(self.aa)
        assert (not self.is_game_over())
        row = action_id // 3
        col = action_id % 3
        assert (self.grid[row, col] == 0)

        self.grid[row, col] = 2
        self.aa.remove(action_id)

        if self.grid[row, 0] == self.grid[row, 1] and self.grid[row, 0] == self.grid[row, 2] or \
                self.grid[0, col] == self.grid[1, col] and self.grid[0, col] == self.grid[2, col] or \
                self.grid[1, 1] == self.grid[0, 0] and self.grid[1, 1] == self.grid[2, 2] and self.grid[1, 1] == 2 or \
                self.grid[2, 0] == self.grid[1, 1] and self.grid[0, 2] == self.grid[1, 1] and self.grid[1, 1] == 2:
            self.current_score = -1.0
            self.game_over = True
            return

        if len(self.aa) == 0:
            self.current_score = 0.0
            self.game_over = True
            return

    def score(self) -> float:
        return self.current_score

    def available_actions_ids(self) -> np.ndarray:
        return np.array(self.aa)

    def reset(self):
        self.grid = np.zeros((3, 3))
        self.game_over = False
        self.aa = [i for i in range(9)]
        self.current_score = 0.0

    def view(self):
        print(f'Score : {self.score()}')
        print(f'Game Over : {self.is_game_over()}')
        for row in range(3):
            for col in range(3):
                c = self.grid[row, col]
                if c == 0:
                    print('_', end='')
                elif c == 1:
                    print('X', end='')
                elif c == 2:
                    print('O', end='')
                else:
                    raise "WTF"
            print()
        print()

    def clone(self):
        new_env = TTTVsRandom()
        new_env.grid = self.grid.copy()
        new_env.aa = self.aa.copy()
        new_env.game_over = self.game_over
        new_env.current_score = self.current_score
        return new_env


def ppo(env: DeepSingleAgentEnv, max_iter_count: int = 10000,
        gamma: float = 0.99,
        learning_rate: float = 1e-5,
        actors_count: int = 10,
        epochs: int = 5,
        c1: float = 1.0,
        c2: float = 0.01):
    pi_and_v_input_state_desc = tf.keras.layers.Input((env.state_dim(),))
    pi_and_v_input_mask = tf.keras.layers.Input((env.max_action_count(),))
    opt = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    hidden_tensor = pi_and_v_input_state_desc
    for _ in range(6):
        hidden_tensor = tf.keras.layers.Dense(128,
                                              activation=tf.keras.activations.tanh,
                                              use_bias=True
                                              )(hidden_tensor)

    output_pi_tensor = tf.keras.layers.Dense(env.max_action_count(),
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

        envs = [env.clone() for _ in range(actors_count)]

        states = np.zeros((actors_count, env.state_dim()))
        masks = np.zeros((actors_count, env.max_action_count()))

        for i, env in enumerate(envs):
            if env.is_game_over():
                if first_episode:
                    ema_score = env.score()
                    first_episode = False
                else:
                    ema_score = (1 - 0.999) * env.score() + 0.999 * ema_score
                    ema_score_progress.append(ema_score)

                env.reset()

            s = env.state_description()

            aa = env.available_actions_ids()

            mask = np.zeros((env.max_action_count(),))
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
            old_score = env.score()
            env.act_with_action_id(chosen_actions[i])
            new_score = env.score()
            r = new_score - old_score

            rewards[i] = r

            s_p = env.state_description()
            aa_p = env.available_actions_ids()

            mask_p = np.zeros((env.max_action_count(),))

            if len(aa_p) > 0:
                mask_p[aa_p] = 1.0

            states_p[i] = s_p
            masks_p[i] = mask_p

            if env.is_game_over():
                game_overs[i] = 0.0

        ### TRAINING TIME !!!

        pi_s_p_pred, v_s_p_pred = model_prediction(pi_and_v_model, [states_p, masks_p])

        targets = tf.constant(rewards + gamma * tf.squeeze(v_s_p_pred) * game_overs)

        deltas = targets - tf.constant(tf.squeeze(v_s_pred))  # for now it's At = Advantage of playing action a
        pi_old = tf.constant(pi_s_pred)

        training_step(pi_and_v_model, [states, masks], chosen_actions, targets, pi_old, deltas, c1, c2, epochs, opt)

    return pi_and_v_model, ema_score_progress


pi_and_v_model, scores = ppo(TTTVsRandom(), max_iter_count=100000)
print(pi_and_v_model.weights)
plt.plot(scores)
plt.show()
