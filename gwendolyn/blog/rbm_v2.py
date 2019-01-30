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

    def optimize(self, v):
        with tf.name_scope('optimization'):
            v0, vk, ph0, phk, _ = self._gibbs_sampling(v)
            dW, db_h, db_v = self._compute_gradients(v0, vk, ph0, phk)
            update_op = self._update_parameter(dW, db_h, db_v)

        with tf.name_scope('accuracy'):
            mask = tf.where(tf.less(v0, 0.0), x=tf.zeros_like(v0), y=tf.ones_like(v0))
            bool_mask = tf.cast(
                tf.where(tf.less(v0, 0.0), x=tf.zeros_like(v0), y=tf.ones_like(v0)),
                dtype=tf.bool,
            )
            acc = tf.where(bool_mask, x=tf.abs(tf.subtract(v0, vk)), y=tf.zeros_like(v0))
            n_values = tf.reduce_sum(mask)
            acc = tf.subtract(1.0, tf.div(tf.reduce_sum(acc), n_values))

        return update_op, acc

    def _update_parameter(self, dW, db_h, db_v):
        alpha = self.FLAGS.learning_rate

        update_op = [
            tf.assign(self.W, alpha*tf.add(self.W, dW)),
            tf.assign(self.bh, alpha*tf.add(self.bh, db_h)),
            tf.assign(self.bv, alpha*tf.add(self.bv, db_v)),
        ]

        return update_op

    def inference(self, v):
        p_h_v = tf.nn.sigmoid(tf.nn.bias_add(tf.matmul(v, self.W), self.bh))
        h_ = self._bernouille_sampling(p_h_v, shape=[1, int(p_h_v.shape[-1])])

        p_v_h = tf.nn.sigmoid(tf.nn.bias_add(tf.matmul(h_, tf.transpose(self.W, [1, 0])), self.bv))
        v_ = self._bernouille_sampling(p_v_h, shape=[1, int(p_v_h.shape[-1])])

        return v_


def main(_):
    num_batches = int(FLAGS.num_samples/FLAGS.batch_size)

    with tf.Graph().as_default():
        train_data, train_data_infer = _get_training_data(FLAGS)
        test_data = _get_test_data(FLAGS)

        iter_train = train_data.make_initializable_iterator()
        iter_train_infer = train_data_infer.make_initializable_iterator()
        iter_test = test_data.make_initializable_iterator()

        x_train = iter_train.get_next()
        x_train_infer = iter_train_infer.get_next()
        x_test = iter_test.get_next()

        model = RBM(FLAGS)
        update_op, accuracy = model.optimize(x_train)
        v_infer = model.inference(x_train_infer)

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for epoch in range(FLAGS.num_epoch):
                acc_train = 0
                acc_infer = 0

                sess.run(iter_train.initializer)

                # training
                for batch_nr in range(num_batches):
                    _, acc = sess.run((update_op, accuracy))
                    acc_train += acc

                    if batch_nr > 0 and batch_nr % FLAGS.eval_after == 0:
                        sess.run(iter_train_infer.initializer)
                        sess.run(iter_test.initializer)

                        num_valid_batches = 0

                        for i in range(FLAGS.num_samples):
                            v_target = sess.run(x_test)[0]

                            if len(v_target[v_target>=0]) > 0:
                                v_ = sess.run(v_infer)[0]
                                acc = 1.0 - np.mean(np.abs(v_[v_target>=0]-v_target[v_target>=0]))
                                acc_infer += acc
                                num_valid_batches += 1
                        print('epoch_nr: %i, batch: %i/%i, acc_train: %.3f, acc_test: %.3f' %
                              (epoch, batch_nr, num_batches,
                               (acc_train/FLAGS.eval_after), (acc_infer/num_valid_batches)))

                        acc_train = 0
                        acc_infer = 0


if __name__ == '__main__':
    main()
