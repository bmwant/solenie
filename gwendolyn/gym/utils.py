import time
import random

import gym
import numpy as np
from IPython.display import clear_output
from gym.envs.registration import register


register(
    id='FrozenLakeNotSlippery-v0',
    entry_point='gym.envs.toy_text:FrozenLakeEnv',
    kwargs={'map_name' : '4x4', 'is_slippery': False},
)


def create_environment():
    env = gym.make('FrozenLakeNotSlippery-v0')
    env.reset()
    return env


def run_game_mc(env, policy, display=True):
    env.reset()
    episode = []
    finished = False

    while not finished:
        s = env.s
        # import pdb; pdb.set_trace()
        if display:
            clear_output(True)  # IPython display
            env.render()
            time.sleep(0.1)

        timestep = []
        timestep.append(s)

        n = random.uniform(0, sum(policy[s].values()))
        top_range = 0
        for prob in policy[s].items():
            top_range += prob[1]
            if n < top_range:
                action = prob[0]
                break

        state, reward, finished, info = env.step(action)
        timestep.append(action)
        timestep.append(reward)
        episode.append(timestep)

    if display:
        clear_output(True)
        env.render()
        time.sleep(0.05)

    return episode


def run_game(env, policy, display=True):
    env.reset()
    episode = []
    finished = False

    while not finished:
        s = env.s
        if display:
            clear_output(True)
            env.render()
            time.sleep(0.5)

        timestep = [s]
        action = policy[s]
        print('Playing action', action)
        state, reward, finished, info = env.step(action)
        timestep.append(action)
        timestep.append(reward)
        episode.append(timestep)

    if display:
        clear_output(True)
        env.render()
        time.sleep(0.5)

    return episode


def test_policy(policy, env):
    wins = 0
    r = 100
    r = 1
    for i in range(r):
        print('Playing game #{}'.format(i+1))
        w = run_game(env, policy, display=True)[-1][-1]
        if w == 1:
            wins += 1
    return wins / r


def argmax_Q(Q, s):
    Q_list = list(map(lambda x: x[1], Q[s].items()))
    indices = [i for i, x in enumerate(Q_list) if x == max(Q_list)]
    return random.choice(indices)


def optimal_policy(Q):
    """
    Derive an optimal policy from optimal values by selecting the highest-
    valued action in each state
    """
    policy = {}
    for state in Q.keys():
        policy[state] = np.argmax(Q[state])
    return policy


def greedy_policy(Q):
    policy = {}
    for state in Q.keys():
        policy[state] = argmax_Q(Q, state)
    return policy


def create_random_policy(env):
    policy = {}
    for key in range(env.observation_space.n):
        current_end = 0
        p = {}
        for action in range(env.action_space.n):
            p[action] = 1 / env.action_space.n
        policy[key] = p
    return policy


def create_state_action_dictionary(env, policy):
    Q = {}
    for key in policy.keys():
        Q[key] = {a: 0.0 for a in range(env.action_space.n)}
    return Q
