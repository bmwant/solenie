# workon solenie
import gym
import numpy as np
from gym import wrappers

env_name = 'Taxi-v2'
env_wrapped = gym.make(env_name)
env = env_wrapped.unwrapped

print('Action space A -> len(A): %d' % env.action_space.n)
print('States space S -> len(S): %d' % env.observation_space.n)


def value_iteration(env, gamma=1.0):
    v = np.zeros(env.observation_space.n)
    max_iterations = 10000
    display_freq = max_iterations // 100
    eps = 1e-20
    last_dif = float('inf')

    print('Starting training loop...')
    for i in range(max_iterations):
        if i % display_freq == 0:
            print('Value function truncated %s' % (v[:25],))
        prev_v = np.copy(v)
        for s in range(env.observation_space.n):
            q_sa = []
            for a in range(env.action_space.n):
                next_states_rewards = []
                for next_sr in env.P[s][a]:
                    p, s_, r, _ = next_sr
                    next_states_rewards.append((p*(r + prev_v[s_])))
                q_sa.append(np.sum(next_states_rewards))
            v[s] = max(q_sa)

        if np.abs(np.abs(np.sum(prev_v - v)) - last_dif) < eps:
            print('Value-iteration converged at iteration %d' % (i+1))
            break
        last_dif = np.abs(np.sum(prev_v -v))
    return v


optimal_value_function = value_iteration(env=env, gamma=1.0)
print('Value function shape: %s\n Value function truncated:\n%s' %
      (optimal_value_function.shape, optimal_value_function[:25]))



def extract_policy(v, gamma=1.0):
    policy = np.zeros(env.observation_space.n)
    for s in range(env.observation_space.n):
        q_sa = np.zeros(env.action_space.n)
        for a in range(env.action_space.n):
            for next_sr in env.P[s][a]:
                p, s_, r, _ = next_sr
                q_sa[a] += (p * (r + gamma * v[s_]))
        policy[s] = np.argmax(q_sa)
    return policy

optimal_policy = extract_policy(v=optimal_value_function, gamma=1.0)
print('Optimal policy shape: %s\n Optimal policy truncated:\n%s' %
      (optimal_policy.shape, optimal_policy[:25]))


def run_episode(env, policy, gamma=1.0, verbose=True, render=False):
    state = env.reset()
    total_reward = 0
    step_idx = 0

    frames = []
    while True:
        if render:
            env.render(mode='human')

        action = int(policy[state])
        state, reward, done, info = env.step(action)
        if verbose:
            print('State: %d - Reward: %d - Done: %d' % (state, reward, done))

        total_reward = total_reward + (gamma ** step_idx * reward)
        step_idx += 1

        if done:
            break
    return total_reward


run_episode(env, optimal_policy, verbose=True, render=True)
