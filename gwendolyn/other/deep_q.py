"""
Play some DOOM here
https://gist.github.com/simoninithomas/7611db5d8a6f3edde269e18b97fa4d0c#file-deep-q-learning-with-doom-ipynb
$ workon solenie3.6
"""
import time
import random
import warnings
from collections import deque

import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
# from vizdoom import *
from skimage import transform
from vizdoom import DoomGame


warnings.filterwarnings('ignore')

stack_size = 4


class Memory(object):
    def __init__(self, max_size):
        self.buffer = deque(maxlen=max_size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        buffer_size = len(self.buffer)
        index = np.random.choice(
            np.arange(buffer_size),
            size=batch_size,
            replace=False
        )
        return [self.buffer[i] for i in index]


class DQNetwork(object):
    def __init__(self, state_size, action_size, learning_rate, name='DQNetwork'):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.name = name

    def model(self):
        with tf.variable_scope(self.name):
            self.inputs_ = tf.placeholder(tf.float32, [None, *self.state_size], name='inputs')
            self.actions_ = tf.placeholder(tf.float32, [None, 3], name='actions_')

            self.target_Q = tf.placeholder(tf.float32, [None], name='target')

            self.conv1 = tf.layers.conv2d(
                inputs=self.inputs_,
                filters=32,
                kernel_size=[8,8],
                strides=[4,4],
                padding='VALID',
                kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d(),
                name='conv1',
            )

            self.conv1_batchnorm = tf.layers.batch_normalization(
                self.conv1,
                training=True,
                epsilon=1e-5,
                name='batch_norm1',
            )

            self.conv1_out = tf.nn.elu(self.conv1_batchnorm, name='conv1_out')

            # Second convnet
            self.conv2 = tf.layers.conv2d(
                inputs=self.conv1_out,
                filters=64,
                kernel_size=[4,4],
                strides=[2,2],
                padding='VALID',
                kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d(),
                name='conv2',
            )

            self.conv2_batchnorm = tf.layers.batch_normalization(
                self.conv2,
                training=True,
                epsilon=1e-5,
                name='batch_norm2',
            )

            self.conv2_out = tf.nn.elu(self.conv2_batchnorm, name='conv2_out')

            # Third convnet

            self.conv3 = tf.layers.conv2d(
                inputs=self.conv2_out,
                filters=128,
                kernel_size=[4,4],
                strides=[2,2],
                padding='VALID',
                kernel_initializer=tf.contrib.layers.xavier_initializer_conv2d(),
                name='conv3',
            )

            self.conv3_batchnorm = tf.layers.batch_normalization(
                self.conv3,
                training=True,
                epsilon=1e-5,
                name='batch_norm3',
            )

            self.conv3_out = tf.nn.elu(self.conv3_batchnorm, name='conv3_out')

            self.flatten = tf.layers.flatten(self.conv3_out)

            self.fc = tf.layers.dense(
                inputs=self.flatten,
                units=512,
                activation=tf.nn.elu,
                kernel_initializer=tf.contrib.layers.xavier_initializer(),
                name='fc1',
            )

            self.output = tf.layers.dense(
                inputs=self.fc,
                kernel_initializer=tf.contrib.layers.xavier_initializer(),
                units=3,
                activation=None,
            )

            self.Q = tf.reduce_sum(tf.multiply(self.output, self.actions_), axis=1)
            self.loss = tf.reduce_mean(tf.square(self.target_Q - self.Q))
            self.optimizer = tf.train.RMSPropOptimizer(self.learning_rate).minimize(self.loss)


def create_environment():
    game = DoomGame()
    game.load_config('basic.cfg')

    game.set_doom_scenario_path('basic.wad')

    game.init()

    left = [1, 0, 0]
    right = [0, 1, 0]
    shoot = [0, 0, 1]
    possible_actions = [left, right, shoot]

    return game, possible_actions


def test_environment():
    game = DoomGame()
    # https://github.com/mwydmuch/ViZDoom/blob/master/scenarios/basic.cfg
    game.load_config('basic.cfg')
    game.set_doom_scenario_path('basic.wad')
    game.init()
    shoot = [0, 0, 1]
    left = [1, 0, 0]
    right = [0, 1, 0]
    actions = [shoot, left, right]

    episodes = 10
    for i in range(episodes):
        game.new_episode()
        while not game.is_episode_finished():
            state = game.get_state()
            img = state.screen_buffer
            misc = state.game_variables
            action = random.choice(actions)
            print('Action', action)
            reward = game.make_action(action)
            print('Reward', reward)
            time.sleep(0.02)
        print('Result', game.get_total_reward())
        time.sleep(2)
    game.close()


def preprocess_frame(frame):
    cropped_frame = frame[30:-10,30:-30]
    normalized_frame = cropped_frame/255.0
    preprocessed_frame = transform.resize(normalized_frame, [84,84])
    return preprocessed_frame


def stack_frames(stacked_frames, state, is_new_episode):
    frame = preprocess_frame(state)

    if is_new_episode:
        stacked_frames = deque([np.zeros((84, 84), dtype=np.int)
                                for i in range(stack_size)], maxlen=4)
        [stacked_frames.append(frame) for _ in range(stack_size)]
    else:
        stacked_frames.append(frame)

    stacked_state = np.stack(stacked_frames, axis=2)

    return stacked_state, stacked_frames



def predict_action(
    sess,
    explore_start,
    explore_stop,
    decay_rate,
    decay_step,
    state,
    possible_actions
):
    exp_exp_tradeoff = np.random.rand()

    explore_probability = explore_stop + (explore_start - explore_stop) * \
                          np.exp(-decay_rate*decay_step)

    if explore_probability > exp_exp_tradeoff:
        # make random action
        action = random.choice(possible_actions)
    else:
        Qs = sess.run(
            DQNetwork.output,
            feed_dict={
                DQNetwork.inputs_: state.reshape((1, *state.shape))
            })
        choice = np.argmax(Qs)
        action = possible_actions[int(choice)]

    return action, explore_probability


def train():
    saver = tf.train.Saver()
    writer = tf.summary.FileWriter('./tensorboard/dqn/1')
    tf.summary.scalar('Loss', DQNetwork.loss)

    write_op = tf.summary.merge_all()

    if training is True:
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            decay_step = 0
            game.init()

            for episode in range(total_episodes):
                step = 0
                episode_rewards = []
                game.new_episode()
                state = game.get_state().screen_buffer

                state, stacked_frames = stacked_frames(stacked_frames, state, True)

                while step < max_steps:
                    step += 1
                    decay_step += 1

                    action, explore_probability = predict_action(
                        explore_start,
                        explore_stop,
                        decay_rate,
                        decay_step,
                        state,
                        possible_actions,
                    )

                    reward = game.make_action(action)
                    done = game.is_episode_finished()
                    episode_rewards.append(reward)

                    if done:
                        next_state = np.zeros((84, 84), dtype=np.int)
                        next_state, stacked_frames = stack_frames(
                            stacked_frames,
                            next_state,
                            False,
                        )

                        step = max_steps

                        total_reward = np.sum(episode_rewards)

                        print('Episode: {}'
                              'Total reward: {}'
                              'Training loss: {:.4f}'
                              'Explore P: {:.4f}'.format(
                            episode, total_reward, loss, explore_probability,
                        ))
                        memory.add((state, action, reward, next_state, done))
                    else:
                        next_state = game.get_state().screen_buffer

                        next_state, stacked_frames = stack_frames(
                            stacked_frames,
                            next_state,
                            False,
                        )

                        memory.add((state, action, reward, next_state, done))
                        state = next_state

                    batch = memory.sample(batch_size)
                    states_mb = np.array([each[0] for each in batch], ndmin=3)
                    actions_mb = np.array([each[1] for each in batch])
                    rewards_mb = np.array([each[2] for each in batch])
                    next_states_mb = np.array([each[3] for each in batch], ndmin=3)
                    dones_mb = np.array([each[4] for each in batch])

                    target_Qs_batch = []

                    Qs_next_state = sess.run(DQNetwork.output,
                                             feed_dict={
                                                 DQNetwork.inputs_: next_states_mb
                                             })

                    for i in range(len(batch)):
                        terminal = dones_mb[i]

                        if terminal:
                            target_Qs_batch.append(rewards_mb[i])
                        else:
                            target = rewards_mb[i] + gamma * np.max(Qs_next_state[i])
                            target_Qs_batch.append(target)
                    targets_mb = np.array([each for each in target_Qs_batch])

                    loss, _ = sess.run([DQNetwork.loss, DQNetwork.optimizer],
                                       feed_dict={
                                           DQNetwork.inputs_: states_mb,
                                           DQNetwork.target_Q: targets_mb,
                                           DQNetwork.actions_: actions_mb,
                                       })
                    summary = sess.run(write_op,
                                       feed_dict={
                                           DQNetwork.inputs_: states_mb,
                                           DQNetwork.target_Q: targets_mb,
                                           DQNetwork.actions_: actions_mb,
                                       })
                    writer.add_summary(summary, episode)
                    writer.flush()
                if episode % 5 == 0:
                    save_path = saver.save(sess, './models/model.ckpt')
                    print('model saved', save_path)



def play(saver, stacked_frames):
    with tf.Session() as sess:
        game, possible_actions = create_environment()

        total_score = 0

        saver.restore(sess, './models/model.ckpt')
        game.init()
        # total episodes
        for i in range(1):
            game.new_episode()
            while not game.is_episode_finished():
                frame = game.get_state().screen_buffer
                # is new episode?
                state = stack_frames(stacked_frames, frame, True)
                Qs = sess.run(
                    DQNetwork.output,
                    feed_dict={
                        DQNetwork.inputs_: state.reshape((1, *state.shape))
                    })
                action = np.argmax(Qs)
                action = possible_actions[int(action)]
                game.make_action(action)
                score = game.get_total_reward()
            print('Score: ', score)
            total_score += score
        print('TOTAL_SCORE', total_score/100.0)
        game.close()


def main():

    stacked_frames = deque([np.zeros((84, 84), dtype=np.int)
                            for i in range(stack_size)], maxlen=4)
    state_size = [84, 84, 4]

    game, possible_actions = create_environment()
    action_size = game.get_available_buttons_size()
    learning_rate = 0.0002

    total_episodes = 500
    max_steps = 100
    batch_size = 64

    # Params for epsilon greedy
    explore_start = 1.0
    explore_stop = 0.01
    decay_reate = 0.0001

    gamma = 0.95

    pretrain_length = batch_size
    memory_size = 1000000

    training = True

    episode_render = False

    tf.reset_default_graph()
    dqn = DQNetwork(state_size, action_size, learning_rate)
    memory = Memory(max_size=memory_size)

    game.new_episode()

    for i in range(pretrain_length):
        if i == 0:
            state = game.get_state().screen_buffer
            state, stacked_frames = stack_frames(stacked_frames, state, True)

        action = random.choice(possible_actions)

        reward = game.make_action(action)

        done = game.is_episode_finished()

        if done:
            next_state = np.zeros(state.shape)
            memory.add((state, action, reward, next_state, done))

            game.new_episode()

            state = game.get_state().screen_buffer
            state, stacked_frames = stack_frames(stacked_frames, state, True)
        else:
            # Get the next state
            next_state = game.get_state().screen_buffer
            next_state, stacked_frames = stack_frames(stacked_frames, next_state, False)

            memory.add((state, action, reward, next_state, done))
            state = next_state


if __name__ == '__main__':
    # test_environment()
    main()
