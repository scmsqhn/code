#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: word_discover_regress.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-10
#   describe:
#================================================================

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
#制造数据，加上随机噪声
import word_discover
from word_discover import *

dig = init_dig('/home/siy/data/广电全量地址_weak.csv')
gen = open_file('/home/siy/data/广电全量地址_weak.csv')


def per(reswds):
    cnt=0
    ls = [len(word) for word in reswds]
    for i in ls:
        if i==1:
            cnt+=1
    return 10*cnt/len(reswds)


x_data =np.linspace(0.0, 30.0, 2000)[:,np.newaxis].reshape(-1,2)
noise = np.random.normal(0, 0.02, x_data.shape)

y_data = []
for item in x_data:
    words_num, qifu_score, reswds = calcu(dig, gen, item[0], item[1])
    print(reswds)
    y_data.append(words_num)
    #y_data.append(per(reswds))
    #y_data.append(np.log(words_num) + \
    #    np.log(qifu_score) + \
    #    np.log(1+per(reswds)))

y_data = np.array(y_data).reshape(-1,1)
#y_data=np.square(x_data)+noise


#定义两层简单的网络
x=tf.placeholder(tf.float32,[None,2])
y=tf.placeholder(tf.float32,[None,1])

w1=tf.Variable(tf.random_normal([2,100]))
b1=tf.Variable(tf.zeros([1,100]))

wx_plus_b1=tf.matmul(x,w1)+b1
l1=tf.nn.tanh(wx_plus_b1)

w2=tf.Variable(tf.random_normal([100,1]))
b2=tf.Variable(tf.zeros([1,1]))

wx_plus_b2=tf.matmul(l1,w2)+b2
predict=tf.nn.tanh(wx_plus_b2)

#pdb.set_trace()

#损失函数选用SME
loss=tf.reduce_mean(tf.square(y-predict))
#优化函数选取梯度下降法
train=tf.train.GradientDescentOptimizer(0.1).minimize(loss)

with tf.Session() as sess:
    predict_y = None
    sess.run(tf.global_variables_initializer())
    for i in range(10):
        print(x_data.shape)
        print(y_data.shape)
        sess.run(train,feed_dict={x:x_data,y:y_data})

    #训练完成后，通过模型得到预测的y值
    predict_y=sess.run(predict,feed_dict={x:x_data})
    print(predict_y)
    pdb.set_trace()
    plt.figure(1)
    plt.scatter(x_data[:,0],y_data)
    plt.plot(x_data[:,0],predict_y,'r',lw=5)
    plt.show()

