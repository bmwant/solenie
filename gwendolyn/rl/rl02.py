import gym
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


env = gym.make('FrozenLake-v0')
lr = 0.1

tf.reset_default_graph()

inputs1 = tf.placeholder(shape=[1, 16], dtype=tf.float32)
W = tf.Variable(tf.random_uniform([16, 4], 0, 0.01))
Q_out = tf.matmul(inputs1, W)
predict = tf.argmax(Q_out, 1)

next_Q = tf.placeholder(shape=[1, 4], dtype=tf.float32)
loss = tf.reduce_sum(tf.square(next_Q - Q_out))
trainer = tf.train.GradientDescentOptimizer(learning_rate=lr)

update_model = trainer.minimize(loss)

# init = tf.initialize_all_variables()
init = tf.initializers.global_variables()

# learning params
y = 0.99
e = 0.1
num_episodes = 2000

# steps per episode
j_list = []
# total rewards
r_list = []
print('Training network...')
with tf.Session() as sess:
    sess.run(init)
    for i in range(num_episodes):
        s = env.reset()
        r_all = 0
        d = False
        j = 0
        while j < 99:
            j += 1
            a, all_Q = sess.run([predict, Q_out], feed_dict={inputs1:np.identity(16)[s:s+1]})
            if np.random.rand(1) < e:
                a[0] = env.action_space.sample()
            # new state, reward, done
            s1, r, d, _ = env.step(a[0])
            Q1 = sess.run(Q_out, feed_dict={inputs1:np.identity(16)[s1:s1+1]})
            max_Q1 = np.max(Q1)
            target_Q = all_Q
            target_Q[0, a[0]] = r + y*max_Q1
            _, W1 = sess.run([update_model, W],
                             feed_dict={
                                 inputs1: np.identity(16)[s:s+1],
                                 next_Q: target_Q
                             })
            r_all += r
            s = s1
            if d is True:
                e = 1.0/((i/50) + 10)
                break
        j_list.append(j)
        r_list.append(r_all)

print('Percent of successful episodes: {}%'.format(sum(r_list)/num_episodes))

plt.plot(r_list)
plt.plot(j_list)
