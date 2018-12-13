"""
Play some DOOM here
https://gist.github.com/simoninithomas/7611db5d8a6f3edde269e18b97fa4d0c#file-deep-q-learning-with-doom-ipynb
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


stack_size = 4
stacked_frames = deque([np.zeros((84, 84), dtype=np.int)
                        for i in range(stack_size)], maxlen=4)


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


if __name__ == '__main__':
    test_environment()
