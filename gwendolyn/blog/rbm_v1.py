"""
python 3.6.5
http://deeplearning.net/software/theano/install_ubuntu.html
"""
import os

import numpy as np
import theano
import theano.tensor as T
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams


class RBM(object):
    def __init__(
            self,
            input_layer=None,
            n_visible=784,
            n_hidden=500,
            W=None,
            hbias=None,
            vbias=None,
            numpy_rng=None,
            theano_rng=None,
    ):
        self.n_visible = n_visible
        self.n_hidden = n_hidden

        if numpy_rng is None:
            numpy_rng = np.random.RandomState(1234)

        if theano_rng is None:
            theano_rng = RandomStreams(numpy_rng.randint(2**30))

        if W is None:
            initial_W = np.asarray(
                numpy_rng.uniform(

                ),
                dtype=theano.config.floatX
            )
            W = theano.shared(value=initial_W, name='W', borrow=True)

        if hbias is None:
            hbias = theano.shared(
                value=np.zeros(
                    n_hidden,
                    dtype=theano.config.floatX
                ),
                name='hbias',
                borrow=True
            )

        if vbias is None:
            vbias = theano.shared(
                value=np.zeros(
                    n_visible,
                    dtype=theano.config.floatX,
                ),
                name='vbias',
                borrow=True,
            )

        if input_layer is None:
            input_layer = T.matrix('input')

        self.input_layer = input_layer
        self.W = W
        self.hbias = hbias
        self.vbias = vbias
        self.theano_rng = theano_rng
        self.params = [self.W, self.hbias, self.vbias]
