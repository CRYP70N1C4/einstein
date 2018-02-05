import tensorflow as tf
import numpy as np


def add_layer(inputs, in_size, out_size, activation_function=None):
    weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    wx_plus_b = tf.matmul(inputs, weights) + biases
    if activation_function is None:
        return wx_plus_b
    else:
        return activation_function(wx_plus_b)


# prepare data
train_X = np.linspace(-1, 1, 300)[:, np.newaxis]
noise = np.random.normal(0, 0.05, train_X.shape)
train_Y = 2 * np.square(train_X) - 0.5 + noise

X = tf.placeholder(tf.float32, [None, 1])
Y = tf.placeholder(tf.float32, [None, 1])

# add hidden layer
layer1 = add_layer(X, 1, 10, activation_function=tf.nn.relu)
# add output layer
prediction = add_layer(layer1, 10, 1)

loss = tf.reduce_mean(tf.reduce_sum(tf.square(train_Y - prediction),reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    for i in range(10000):
        session.run(train_step, feed_dict={X: train_X, Y: train_Y})
        if i % 500 == 0:
            print(session.run(loss, feed_dict={X: train_X, Y: train_Y}))
