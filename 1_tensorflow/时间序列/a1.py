from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.contrib.timeseries.python.timeseries import NumpyReader

train_X = np.arange(0, 1000);
noise = np.random.uniform(-0.2, 0.2, 1000)
train_Y = np.sin(np.pi * train_X / 100) + train_X / 200. + noise

data = {
    tf.contrib.timeseries.TrainEvalFeatures.TIMES: train_X,
    tf.contrib.timeseries.TrainEvalFeatures.VALUES: train_X,
}

reader = NumpyReader(data)


train_input_fn = tf.contrib.timeseries.RandomWindowInputFn(
    reader, batch_size=2, window_size=10)

with tf.Session() as sess:
    batch_data = train_input_fn.create_batch()
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    one_batch = sess.run(batch_data[0])
    coord.request_stop()

print('one_batch_data:', one_batch)