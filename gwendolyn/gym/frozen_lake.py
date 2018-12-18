"""
https://harderchoices.com/2018/04/04/monte-carlo-method-in-python/
$ workon solenie
"""
import random

from gwendolyn.gym.utils import (
    run_game,
    test_policy,
    create_environment,
    create_random_policy,
    create_state_action_dictionary,
)


def test_env(env):
    done = False
    while not done:
        env.render()
        action = env.action_space.sample()
        print('Action', action)
        observation, reward, done, info = env.step(action)


def monte_carlo_e_soft(env, episodes=100, policy=None, epsilon=0.01):
    if not policy:
        policy = create_random_policy(env)

    Q = create_state_action_dictionary(env, policy)
    result = {}

    for _ in range(episodes):
        G = 0  # cumulative reward
        episode = run_game(env=env, policy=policy, display=False)
        for i in reversed(range(len(episode))):
            s_t, a_t, r_t = episode[i]
            state_action = (s_t, a_t)
            G += r_t

            if not state_action in [(x[0], x[1]) for x in episode[0:i]]:
                if result.get(state_action):
                    result[state_action].append(G)
                else:
                    result[state_action] = [G]

                Q[s_t][a_t] = sum(result[state_action]) / len(result[state_action])

                Q_list = list(map(lambda x: x[1], Q[s_t].items()))
                indices = [i for i, x in enumerate(Q_list) if x == max(Q_list)]
                max_Q = random.choice(indices)

                A_star = max_Q

                for a in policy[s_t].items():
                    if a[0] == A_star:
                        policy[s_t][a[0]] = 1 - epsilon + (epsilon / abs(sum(policy[s_t].values())))
                    else:
                        policy[s_t][a[0]] = (epsilon / abs(sum(policy[s_t].values())))
    return policy


def main():
    env = create_environment()
    pol = create_random_policy(env)
    print(pol)
    Q = create_state_action_dictionary(env, pol)
    print(Q)
    # test_env(env)
    # policy = monte_carlo_e_soft(env, episodes=200)
    # print(test_policy(policy, env))
    # run_game(env, policy)


if __name__ == '__main__':
    main()
