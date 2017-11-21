import tensorflow as tf
import numpy as np

# prepare train data
train_X = np.linspace(-1, 1, 100)
train_Y = 2 * train_X + np.random.randn(*train_X.shape) * 0.33 + 10

# define model
X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)
w = tf.Variable(0.0, name="weight")
b = tf.Variable(0.0, name="bias")
loss = tf.square(Y - w * X - b)
train_op = tf.train.GradientDescentOptimizer(0.01).minimize(loss)



with tf.Session() as session:
    session.run(tf.global_variables_initializer())
    epoch = 1
    for i in range(50):
        for (x, y) in zip(train_X, train_Y):
            _, loss_value, w_value, b_value = session.run([train_op, loss, w, b],
                                                          feed_dict={X: x, Y: y})
        epoch += 1
        if i % 5 == 0:
            print("Epoch: {}，loss:{} w: {}, b: {}".format(epoch, loss_value, w_value, b_value))
