#!

import pdb
import tensorflow as tf
import numpy as np
#生成一千个点
global saver


def train():
    x_data=np.random.random([1000,3])
    y_data=np.matmul(x_data,[[2],[3],[2]])+[1.]
    x=tf.placeholder(tf.float32,[None,3],name='x')
    y=tf.placeholder(tf.float32,[None,1],name='y')
    weight=tf.Variable(tf.random_normal([3,1]),dtype=tf.float32)
    bias=tf.Variable(tf.ones([1]),dtype=tf.float32)
    y_label=tf.add(tf.matmul(x,weight),bias)
    loss=tf.reduce_mean(tf.square(y-y_label))
    train=tf.train.GradientDescentOptimizer(0.2).minimize(loss)
    return train,x,y,x_data,loss,y_data,y_label

def sess_run(train,x,y,x_data,loss,y_data,y_label):
    saver = tf.train.Saver()
    with tf.Session() as sess:
    #变量初始化，目的是给Graph上的图中的变量初始化。
        sess.run(tf.global_variables_initializer())
        for i in range(1000):
            y_label = sess.run(train,feed_dict={x:x_data,y:y_data})
            if(i%100==0):
                print(sess.run(loss,feed_dict={x:x_data,y:y_data}))
        #tf.add_to_collection('y_', y_label)
        tf.add_to_collection('y', y)
        tf.add_to_collection('x', x)
        saver.save(sess,'ckpt/cele_model')
        saver.save(sess,'/root/yunyan/src/business_ultra/ckpt/cele_model')

def sess_pred():
    saver = tf.train.import_meta_graph('/root/yunyan/src/business_ultra/ckpt/cele_model.meta')
    weight = np.random.random([1000,3])
    bias = np.random.random([1000,1])
    with tf.Session() as sess:
        saver.restore(sess, '/root/yunyan/src/business_ultra/ckpt/cele_model')
        graph = tf.get_default_graph()
        x = graph.get_operation_by_name('x').outputs[0]
        y = graph.get_operation_by_name('y').outputs[0]
        #y_ = graph.get_operation_by_name('y_').outputs[0]
        return sess.run(y, feed_dict={x:weight,y:bias})

if __name__ == '__main__':
    res = train()
    sess_run(*res)
    sess_pred()

