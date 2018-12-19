"""
https://github.com/jknthn/learning-rl/blob/master/td-learning.ipynb
$ workon solenie
"""
import random
import numpy as np

from gwendolyn.gym.utils import (
    test_policy,
    greedy_policy,
    create_environment,
    create_random_policy,
    create_state_action_dictionary,
)


def double_Q_learning(env, episodes=100, step_size=0.01, exploration_rate=0.01):
    policy = create_random_policy(env)

    Q_1 = create_state_action_dictionary(env, policy)
    Q_2 = create_state_action_dictionary(env, policy)

    def update_Q(q_upd, q_other, s, a, s_, reward):
        """Update rule"""
        q_upd[s][a] = q_upd[s][a] + step_size * \
                  (reward + exploration_rate*max(q_other[s_].values()) - q_upd[s][a])

    for episode in range(episodes):
        env.reset()
        S = env.s
        done = False

        while not done:
            Q = {
                s: {a: av + Q_2[s][a] for a, av in sv.items()}
                for s, sv in Q_1.items()
            }
            A = greedy_policy(Q, consistent=False)[S]
            S_prime, reward, done, _ = env.step(A)

            if random.random() < 0.5:
                # update_Q(Q_1, Q_2, S, A, S_prime, reward)
                Q_1[S][A] = Q_1[S][A] + step_size * (reward + exploration_rate * max(Q_2[S_prime].values()) - Q_1[S][A])
            else:
                # update_Q(Q_2, Q_1, A, A, S_prime, reward)
                Q_2[S][A] = Q_2[S][A] + step_size * (reward + exploration_rate * max(Q_1[S_prime].values()) - Q_2[S][A])
            S = S_prime

    # Sum values for all the states from Q_1 and Q_2
    Q = {
        s: {a: av + Q_2[s][a] for a, av in sv.items()}
        for s, sv in Q_1.items()
    }
    return greedy_policy(Q), Q


if __name__ == '__main__':
    env = create_environment()
    policy, Q = double_Q_learning(
        env,
        episodes=400,
        step_size=0.3,
        exploration_rate=0.2,
    )
    print(policy)
    print(Q)
    print(test_policy(policy, env))
