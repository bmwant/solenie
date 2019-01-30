"""
https://www.cs.toronto.edu/~rsalakhu/papers/rbmcf.pdf
https://towardsdatascience.com/deep-learning-meets-physics-restricted-boltzmann-machines-part-ii-4b159dce1ffb
"""
import tensorflow as tf


class RBM(object):
    def __init__(self, FLAGS):
        self.FLAGS = FLAGS
        self.weight_initializer = model_helper._get_weight_init()
        self.bias_initializer = model_helper._get_bias_init()
        self.init_parameter()

    def init_parameter(self):
        with tf.variable_scope('Network_parameter'):
            self.W = tf.get_variable(
                'Weights',
                shape=(self.FLAGS.num_v, self.FLAGS.num_h),
                initializer=self.weight_initializer,
            )
            self.bh = tf.get_variable(
                'hidden_bias',
                shape=(self.FLAGS.num_h),
                initializer=self.bias_initializer,
            )
            self.bv = tf.get_variable(
                'visible_bias',
                shape=(self.FLAGS.num_v),
                initializer=self.bias_initializer,
            )

    def _sample_h(self, v):
        with tf.name_scope('sampling_hidden_units'):
            a = tf.nn.bias_add(tf.matmul(v, self.W), self.bh)
            p_h_v = tf.nn.sigmoid(a)
            h_ = self._bernouille_sampling(
                p_h_v,
                shape=(self.FLAGS.batch_size, int(p_h_v.shape[-1]))
            )
            return p_h_v, h_

    def _bernouille_sampling(self, p, shape):
        return tf.where(
            tf.less(p, tf.random_uniform(shape, minval=0.0, maxval=1.0)),
            x=tf.zeros_like(p),
            y=tf.ones_like(p),
        )

    def _sample_v(self, h):
        with tf.name_scope('sampling_visible_units'):
            a = tf.nn.bias_add(tf.matmul(h, tf.transpose(self.W, [1, 0])), self.bv)
            p_v_h = tf.nn.sigmoid(a)
            v_ = self._bernouille_sampling(
                p_v_h,
                shape=(self.FLAGS.batch_size, int(p_v_h.shape[-1])),
            )
            return p_v_h, v_

    def _gibbs_sampling(self, v):
        def condition(i, vk, hk, v):
            r = tf.less(i, k)
            return r[0]

        def body(i, vk, hk, v):
            _, hk = self._sample_h(vk)
            _, vk = self._sample_v(hk)

            vk = tf.where(tf.less(v, 0), v, vk)

            return [i+1, vk, hk, v]

        ph0, _ = self._sample_h(v)

        vk = v
        hk = tf.zeros_like(ph0)
        i = 0
        k = tf.constant([self.FLAGS.k])

        [i, vk, hk, v] = tf.while_loop(condition, body, [i, vk, hk, v])

        phk, _ = self._sample_h(vk)

        return v, vk, ph0, phk, i

    def _compute_gradients(self, v0, vk, ph0, phk):
        def condition(i, v0, vk, ph0, phk, dW, db_h, db_v):
            r = tf.less(i, k)
            return r[0]

        def body(i, v0, vk, ph0, phk, dW, dbh, dbv):
            v0_ = v0[i]
            ph0_ = ph0[i]

            vk_ = vk[i]
            phk_ = phk[i]

            ph0_ = tf.reshape(ph0_, [1, self.FLAGS.num_h])
            v0_ = tf.reshape(v0_, [self.FLAGS.num_v, 1])
            phk_ = tf.reshape(phk_, [1, self.FLAGS.num_h])
            vk_ = tf.reshape(vk_, [self.FLAGS.num_v, 1])

            # calculating the gradients for weights
            dw_ = tf.subtract(tf.multiply(ph0_, v0_), tf.multiply(phk_, vk_))
            # calculating the gradients for hidden bias
            dbh_ = tf.subtract(ph0_, phk_)
            dbv_ = tf.subtract(v0_, vk_)

            dbh_ = tf.reshape(dbh_, [self.FLAGS.num_h])
            dbv_ = tf.reshape(dbv_, [self.FLAGS.num_v])

            return [i+1, v0, vk, ph0, phk, tf.add(dW, dw_), tf.add(dbh, dbh_), tf.add(dbv, dbv_)]

        i = 0
        k = tf.constant([self.FLAGS.batch_size])
        dW = tf.zeros((self.FLAGS.num_v, self.FLAGS.num_h))
        dbh = tf.zeros((self.FLAGS.num_h,))
        dbv = tf.zeros((self.FLAGS.num_v,))

        [i, v0, vk, ph0, phk, dW, db_h, db_v] = tf.while_loop(
            condition, body,
            [i, v0, vk, ph0, phk, dW, dbh, dbv],
        )
        dW = tf.div(dW, self.FLAGS.batch_size)
        dbh = tf.div(dbh, self.FLAGS.batch_size)
        dbv = tf.div(dbv, self.FLAGS.batch_size)

        return dW, dbh, dbv
