import os
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
