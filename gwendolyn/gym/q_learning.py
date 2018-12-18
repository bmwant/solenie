"""
https://github.com/jknthn/learning-rl/blob/master/td-learning.ipynb
$ workon solenie
"""
from gwendolyn.gym.utils import (
    greedy_policy,
    test_policy,
    create_environment,
    create_random_policy,
    create_state_action_dictionary,
)


def Q_learning(env, episodes=100, step_size=0.01, exploration_rate=0.01):
    policy = create_random_policy(env)
    Q = create_state_action_dictionary(env, policy)

    for episode in range(episodes):
        env.reset()
        S = env.s
        done = False

        while not done:
            A = greedy_policy(Q)[S]
            S_prime, reward, done, _ = env.step(A)
            Q[S][A] = Q[S][A] + step_size * \
                      (reward + exploration_rate * max(Q[S_prime].values()) - Q[S][A])
            S = S_prime

    return greedy_policy(Q), Q


if __name__ == '__main__':
    env = create_environment()
    policy, Q = Q_learning(
        env,
        episodes=200,
        step_size=0.1,
        exploration_rate=0.2,
    )
    print(policy)
    print(Q)
    print(test_policy(policy, env))
