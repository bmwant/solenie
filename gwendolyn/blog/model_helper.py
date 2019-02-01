import os
import gzip
import pickle
import numpy as np
import tensorflow as tf


def get_bias_init():
    return tf.zeros_initializer()


def get_weight_init():
    return tf.random_normal_initializer(mean=0.0, stddev=0.5)


def get_training_data(FLAGS):
    filenames = [FLAGS.tf_records_train_path+f for f in os.listdir(FLAGS.tf_records_train_path)]

    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.map(parse)
    dataset = dataset.shuffle(buffer_size=500)
    dataset = dataset.repeat()
    dataset = dataset.batch(FLAGS.batch_size)
    dataset = dataset.prefetch(buffer_size=1)

    dataset2 = tf.data.TFRecordDataset(filenames)
    dataset2 = dataset2.map(parse)
    dataset2 = dataset2.shuffle(buffer_size=1)
    dataset2 = dataset2.repeat()
    dataset2 = dataset2.batch(1)
    dataset2 = dataset2.prefetch(buffer_size=1)

    return dataset, dataset2


def get_test_data(FLAGS):
    filenames = [FLAGS.tf_records_test_path+f for f in os.listdir(FLAGS.tf_records_test_path)]

    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.map(parse)
    dataset = dataset.shuffle(buffer_size=1)
    dataset = dataset.repeat()
    dataset = dataset.batch(1)
    dataset = dataset.prefetch(buffer_size=1)

    return dataset


def parse(serialized):
    features = {
        'movie_ratings': tf.FixedLenFeature([3952], tf.float32),
    }

    parsed_example = tf.parse_single_example(
        serialized,
        features=features,
    )

    movie_ratings = tf.cast(parsed_example['movie_ratings'], tf.float32)

    return movie_ratings


def load_data(dataset):
    import theano
    import theano.tensor as T

    data_dir, data_file = os.path.split(dataset)
    if data_dir == '' and not os.path.isfile(dataset):
        new_path = os.path.join(
            os.path.split(__file__)[0],
            '..',
            'data',
            dataset
        )
        if os.path.isfile(new_path) or data_file == 'mnist.pkl.gz':
            dataset = new_path

    if (not os.path.isfile(dataset)) and data_file == 'mnist.pkl.gz':
        from six.moves import urllib
        origin = 'http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz'
        print('Downloading data from %s' % origin)
        urllib.request.urlretrieve(origin, dataset)

    print(' ... loading data')

    with gzip.open(dataset, 'rb') as f:
        try:
            train_set, valid_set, test_set = pickle.load(f, encoding='latin1')
        except Exception:
            train_set, valid_set, test_set = pickle.load(f)

    def shared_dataset(data_xy, borrow=True):
        data_x, data_y = data_xy
        shared_x = theano.shared(
            np.asarray(data_x, dtype=theano.config.floatX),
            borrow=borrow,
        )
        shared_y = theano.shared(
            np.asarray(data_y, dtype=theano.config.floatX),
            borrow=borrow,
        )
        return shared_x, T.cast(shared_y, 'int32')

    test_set_x, test_set_y = shared_dataset(test_set)
    valid_set_x, valid_set_y = shared_dataset(valid_set)
    train_set_x, train_set_y = shared_dataset(train_set)

    rval = [
        (train_set_x, train_set_y),
        (valid_set_y, valid_set_y),
        (test_set_x, test_set_y),
    ]

    return rval


def tile_raster_images(X, img_shape, tile_shape, tile_spacing=(0, 0),
                       scale_rows_to_unit_interval=True,
                       output_pixel_vals=True):
    assert len(img_shape) == 2
    assert len(tile_shape) == 2
    assert len(tile_spacing) == 2

    out_shape = [
        (ishp + tsp) * tshp - tsp
        for ishp, tshp, tsp, in zip(img_shape, tile_shape, tile_spacing)
    ]

    if isinstance(X, tuple):
        assert len(X) == 4
        if output_pixel_vals:
            out_array = np.zeros((out_shape[0], out_shape[1], 4), dtype='uint8')
        else:
            out_array = np.zeros((out_shape[0], out_shape[1], 4), dtype=X.dtype)

        if output_pixel_vals:
            channel_defaults = [0, 0, 0, 255]
        else:
            channel_defaults = [0., 0., 0., 1.]

        for i in range(4):
            if X[i] is None:
                dt = out_array.dtype
                if output_pixel_vals:
                    dt = 'uint8'
                out_array[:, :, i] = np.zeros(
                    out_shape,
                    dtype=dt,
                ) + channel_defaults[i]
            else:
                out_array[:, :, i] = tile_raster_images(
                    X[i], img_shape, tile_shape, tile_spacing,
                    scale_rows_to_unit_interval, output_pixel_vals
                )
        return out_array

    else:
        H, W = img_shape
        Hs, Ws = tile_spacing

        dt = X.dtype
        if output_pixel_vals:
            dt = 'uint8'
        out_array = np.zeros(out_shape, dtype=dt)

        for tile_row in range(tile_shape[0]):
            for tile_col in range(tile_shape[1]):
                if tile_row * tile_shape[1] + tile_col < X.shape[0]:
                    this_x = X[tile_row * tile_shape[1] + tile_col]
                    if scale_rows_to_unit_interval:
                        this_img = scale_to_unit_interval(
                            this_x.reshape(img_shape)
                        )
                    else:
                        this_img = this_x.reshape(img_shape)
                    c = 1
                    if output_pixel_vals:
                        c = 255
                    out_array[
                        tile_row * (H + Hs): tile_row * (H + Hs) + H,
                        tile_col * (W + Ws): tile_col * (W + Ws) + W,
                    ] = this_img * c
        return out_array


def scale_to_unit_interval(ndar, eps=1e-8):
    ndar = ndar.copy()
    ndar -= ndar.min()
    ndar *= 1.0 / (ndar.max() + eps)
    return ndar
