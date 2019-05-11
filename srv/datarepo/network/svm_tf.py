#!encoding=utf-8

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn import datasets
import pdb

class MySVM(object):
    def init(self):
        self.sess = tf.Session()
        self.init_data()
        self.init_feed_in()
        self.init_stru()
        # iris.data = [(Sepal Length, Sepal Width, Petal Length, Petal Width)]

    def init_data(self):
        #iris = datasets.load_iris()
        #x_vals = np.array([[x[0], x[0], x[5]] for x in iris.data])
        #y_vals = np.array([1 if y == 0 else -1 for y in iris.target])

        #train_indices = np.random.choice(len(x_vals),
                                 #round(len(x_vals)*0.8),
                                 #replace=False)

        #test_indices = np.array(list(set(range(len(x_vals))) - set(train_indices)))
        #self.x_vals_train = x_vals[train_indices]
        #self.x_vals_test = x_vals[test_indices]
        #self.y_vals_train = y_vals[train_indices]
        #self.y_vals_test = y_vals[test_indices]

        self.batch_size = 1
        self.vec = 5

    def init_feed_in(self):
        self.x_data = tf.placeholder(shape=[None, self.vec], dtype=tf.float32)
        self.y_target = tf.placeholder(shape=[None, 1], dtype=tf.float32)

    def init_stru(self):
        A = tf.Variable(tf.random_normal(shape=[self.vec, 1]))
        b = tf.Variable(tf.random_normal(shape=[1, 1]))
        """key part of this module the A matmul make the svm work"""
        model_output = tf.subtract(tf.matmul(self.x_data, A), b)
        l2_norm = tf.reduce_sum(tf.square(A))
        # Loss = max(0, 1-pred*actual) + alpha * L2_norm(A)^2
        alpha = tf.constant([0.01])
        classification_term = tf.reduce_mean(tf.maximum(0., tf.subtract(1., tf.multiply(model_output, self.y_target))))
        loss = tf.add(classification_term, tf.multiply(alpha, l2_norm))
        my_opt = tf.train.GradientDescentOptimizer(0.01)
        self.train_step = my_opt.minimize(loss)
        self.init = tf.global_variables_initializer()
        self.A = A
        self.b = b

    def step(self,x,y):
        self.sess.run(
            self.train_step,
            feed_dict={self.x_data: x, self.y_target: y})
        _A = self.sess.run(self.A)
        _b = self.sess.run(self.b)
        print('A,b: ',_A,_b)

    def run(self):
        self.sess.run(self.init)
        loss_vec = []
        train_accuracy = []
        test_accuracy = []
        #for i in range(20000):
            #rand_index = np.random.choice(len(self.x_vals_train), size=self.batch_size)
            #print(rand_index)
            #rand_x = self.x_vals_train[rand_index]
            #rand_y = np.transpose([self.y_vals_train[rand_index]])


"""
pic
[[a1], [a2], [a3]] = sess.run(A)
[[b]] = sess.run(b)
slope = -a3/a1
y_intercept = b/a1
best_fit = []

x1_vals = [d[2] for d in x_vals]

for i in x1_vals:
    best_fit.append(slope*i+y_intercept)


# Separate I. setosa
setosa_x = [d[2] for i, d in enumerate(x_vals) if y_vals[i] == 1]
setosa_y = [d[0] for i, d in enumerate(x_vals) if y_vals[i] == 1]
not_setosa_x = [d[2] for i, d in enumerate(x_vals) if y_vals[i] == -1]
not_setosa_y = [d[0] for i, d in enumerate(x_vals) if y_vals[i] == -1]
print(not_setosa_x)
print(not_setosa_y)

plt.plot(setosa_x, setosa_y, 'o', label='I. setosa')
plt.plot(not_setosa_x, not_setosa_y, 'x', label='Non-setosa')
plt.plot(x1_vals, best_fit, 'r-', label='Linear Separator', linewidth=3)
plt.ylim([0, 10])
plt.legend(loc='lower right')
plt.title('Sepal Length vs Pedal Width')
plt.xlabel('Pedal Width')
plt.ylabel('Sepal Length')
plt.show()

"""

