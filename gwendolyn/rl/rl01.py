# https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-0-q-learning-with-tables-and-neural-networks-d195264329d0
import gym
import numpy as np

env = gym.make('FrozenLake-v0')

Q = np.zeros([env.observation_space.n, env.action_space.n])
lr = 0.8
y = 0.95

num_episodes = 2000

r_list = []
for i in range(num_episodes):
    s = env.reset()  # environment state
    r_all = 0  # total reward
    d = False  # done?
    j = 0  # iteration number
    while j < 99:
        j += 1
        # choose an action (e-greedy)
        a = np.argmax(Q[s,:] +
                      np.random.randn(1, env.action_space.n)*(1.0/(i+1)))
        # new state
        s1, r, d, _ = env.step(a)
        Q[s, a] = Q[s, a] + lr*(r + y*np.max(Q[s1,:]) - Q[s, a])
        r_all += r
        # prev state now equals current state
        s = s1
        if d is True:
            break
    # store all the rewards
    r_list.append(r_all)


print('Avg score over time: ', sum(r_list) / num_episodes)
print('Final Q table values')
print(Q)
