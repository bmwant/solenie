"""
https://harderchoices.com/2018/06/07/temporal-difference-learning-in-python/
$ workon solenie
"""
from gwendolyn.gym.utils import (
    test_policy,
    greedy_policy,
    create_environment,
    create_random_policy,
    create_state_action_dictionary,
)


def sarsa(env, episodes=100, step_size=0.01, exploration_rate=0.01):
    policy = create_random_policy(env)
    Q = create_state_action_dictionary(env, policy)

    for episode in range(episodes):
        env.reset()
        S = env.s
        A = greedy_policy(Q)[S]
        done = False

        while not done:
            S_prime, reward, done, _ = env.step(A)
            A_prime = greedy_policy(Q)[S_prime]
            Q[S][A] = Q[S][A] + step_size * \
                      (reward + exploration_rate * Q[S_prime][A_prime] - Q[S][A])

            S = S_prime
            A = A_prime

    return greedy_policy(Q), Q


if __name__ == '__main__':
    env = create_environment()
    policy, Q = sarsa(
        env,
        episodes=200,
        step_size=0.1,
        exploration_rate=0.2,
    )
    print(policy)
    print(Q)
    print(test_policy(policy, env))
