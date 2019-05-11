#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: word_discover_tensor.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-10
#   describe:
#================================================================


import math
import word_discover
from word_discover import *
from matplotlib import pyplot as plt
import os
import numpy as np
import pandas as pd
from sklearn import metrics
import tensorflow as tf
from tensorflow.python.data import Dataset
import pickle
import pdb

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

tf.logging.set_verbosity(tf.logging.ERROR)  # DEBUG INFO WARN ERROR FATAL

# init vocab
vocab = word_discover.vocab('/home/siy/data/广电全量地址_weak.csv')
dig = word_discover.init_dig('/home/siy/data/广电全量地址_weak.csv')
connect_table = dig_2_table(dig)

pickle.dump((dig,vocab,connect_table), open('pk.pkl','wb+'))
# save the Dig vocab and connect_table


pd.options.display.max_rows = 10
pd.options.display.max_columns = 9
# pd.set_option('max_columns', 9)
pd.options.display.float_format = '{:.1f}'.format


import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
#制造数据，加上随机噪声
# x_data = np.linspace(-0.5, 0.5, 200)[:,np.newaxis]
x_data = np.array(connect_table.fillna(0.0))

#noise = np.random.normal(0, 0.02, x_data.shape)
#y_data=np.square(x_data)+noise
y_daya =0.0

#定义两层简单的网络

shape = list(connect_table.shape)
print(shape)
x=tf.placeholder(tf.float32,[None, shape[0], shape[1]])
y=tf.placeholder(tf.float32,[None, 1])

w1=tf.Variable(tf.random_normal([shape[0],shape[1]]))
b1=tf.Variable(tf.zeros([shape[0],shape[1]]))

wx_plus_b1=tf.matmul(x,w1)+b1
l1=tf.nn.tanh(wx_plus_b1)

w2=tf.Variable(tf.random_normal([shape[1],1]))
b2=tf.Variable(tf.zeros([shape[1],1]))

wx_plus_b2=tf.matmul(l1,w2)+b2
predict=tf.nn.tanh(wx_plus_b2)

#损失函数选用SME
loss=tf.reduce_mean(tf.square(y-predict))
#优化函数选取梯度下降法
train=tf.train.GradientDescentOptimizer(0.1).minimize(loss)

with tf.Session() as sess:
    predict_y = None
    sess.run(tf.global_variables_initializer())
    for i in range(2000):
        sess.run(train,feed_dict={x:x_data,y:y_data})

    #训练完成后，通过模型得到预测的y值
    predict_y=sess.run(predict,feed_dict={x:x_data})
    plt.figure()
    plt.scatter(x_data,y_data)
    plt.plot(x_data,predict_y,'r',lw=5)
    plt.show()
---------------------
作者：zcc_TPJH
来源：CSDN
原文：https://blog.csdn.net/weixin_39881922/article/details/80551181
版权声明：本文为博主原创文章，转载请附上博文链接！














#===============================================================

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)







def my_model(features, labels, mode, params):
    """DNN with three hidden layers, and dropout of 0.1 probability."""
    # 定义模型结构
    # input layer
    net = tf.feature_column.input_layer(features, params['feature_columns'])
    # hidden layers, sized according to the 'hidden_units' param.
    for units in params['hidden_units']:
        net = tf.layers.dense(net, units=units, activation=tf.nn.relu)
    # output layer, Compute logits (1 per class).
    logits = tf.layers.dense(net, params['n_classes'], activation=None)

    # Compute predictions.
    predicted_classes = tf.argmax(logits, 1)
    # 若调用predict方法
    if mode == tf.estimator.ModeKeys.PREDICT:
        predictions = {
            'class_ids': predicted_classes[:, tf.newaxis],
            'probabilities': tf.nn.softmax(logits),
            'logits': logits,
        }
        return tf.estimator.EstimatorSpec(mode, predictions=predictions)

    # Compute loss.
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)
    # Compute evaluation metrics.
    accuracy = tf.metrics.accuracy(labels=labels,
                                   predictions=predicted_classes,
                                   name='acc_op')
    metrics = {'accuracy': accuracy}
    tf.summary.scalar('accuracy', accuracy[1])
    # 若调用evaluate方法
    if mode == tf.estimator.ModeKeys.EVAL:
        return tf.estimator.EstimatorSpec(
            mode, loss=loss, eval_metric_ops=metrics)

    # 若调用train方法
    # Create training op.
    assert mode == tf.estimator.ModeKeys.TRAIN

    optimizer = tf.train.AdagradOptimizer(learning_rate=0.1)
    train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())
    return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op)
---------------------
作者：流水空间
来源：CSDN
原文：https://blog.csdn.net/liushuikong/article/details/79223407
版权声明：本文为博主原创文章，转载请附上博文链接！




'''




# 加载数据集
# california_housing_dataframe = pd.read_csv
# ("https://storage.googleapis.com/mledu-datasets/california_housing_train.csv", sep=',')
california_housing_dataframe = pd.read_csv("california_housing_train.csv", sep=',')

# 随机数据
california_housing_dataframe = california_housing_dataframe.reindex(
    np.random.permutation(california_housing_dataframe.index))

# 将数据整合到统一范围，median_house_value单位为千记
california_housing_dataframe["median_house_value"] /= 1000.0

# 检查数据
# print('\n数据：')
# print(california_housing_dataframe.head())
# print('\n数据统计：')
# describe = california_housing_dataframe.describe()
# print(describe)

# 搞模型

# 1.定义特征和特征列
my_feature = california_housing_dataframe[['total_rooms']]  # 返回dataframe
# my_feature_series = california_housing_dataframe['total_rooms']  # 返回series
# print('\n特征')
# print(type(my_feature))
# print(type(my_feature_series))
feature_columns = [tf.feature_column.numeric_column('total_rooms')]  # 定义特征列 todo
# print(feature_columns)


# 2.定义目标
targets = california_housing_dataframe['median_house_value']

# 3.配置线性回归
my_optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-3)
my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)
linear_regressor = tf.estimator.LinearRegressor(feature_columns=feature_columns, optimizer=my_optimizer)


# 4.定义输入函数
def my_input_fn(features, targets, batch_size=1, shuffle=True, num_epochs=None):
    """
    输入函数
    :param features: 输入特征
    :param targets: 数据标签
    :param batch_size: 输出数据的大小
    :param shuffle: 随机抽取数据
    :param num_epochs:重复的次数
    :return:数据和标签
    """
    features = {key: np.array(value) for key, value in dict(features).items()}

    ds = Dataset.from_tensor_slices((features, targets))
    ds = ds.batch(batch_size).repeat(num_epochs)

    if shuffle:
        ds = ds.shuffle(buffer_size=10000)

    features, labels = ds.make_one_shot_iterator().get_next()
    return features, labels


# 5.训练
_ = linear_regressor.train(input_fn=lambda: my_input_fn(my_feature, targets), steps=100)

# 6.评估模型
prediction_input_fn = lambda: my_input_fn(my_feature, targets, num_epochs=1, shuffle=False)
predictions = linear_regressor.predict(input_fn=prediction_input_fn)

predictions = np.array([item['predictions'][0] for item in predictions])
# print(predictions)

# 6.评估误差
mean_squared_error = metrics.mean_squared_error(targets, predictions)
root_mean_squared_error = math.sqrt(mean_squared_error)

min_house_value = california_housing_dataframe['median_house_value'].min()
max_house_value = california_housing_dataframe['median_house_value'].max()
max_min_difference = max_house_value - min_house_value

# print('Mean squared error(on train set): %.3f' % mean_squared_error)
print('Root mean squared error(on train set): %.3f' % root_mean_squared_error)
print('Max. median house value(on train set): %.3f' % max_house_value)
print('Min. median house value(on train set): %.3f' % min_house_value)
print('Difference between Min. and Max.(on train set): %.3f' % max_min_difference)

# 方差大，校准数据
# Root mean squared error(on train set): 237.417
# Max. median house value(on train set): 500.001
# Min. median house value(on train set): 14.999
# Difference between Min. and Max.(on train set): 485.002
calibration_data = pd.DataFrame()
calibration_data['prediction'] = pd.Series(predictions)
calibration_data['targets'] = pd.Series(targets)
print(calibration_data.describe())
#        prediction  targets
# count     17000.0  17000.0
# mean          0.1    207.3
# std           0.1    116.0
# min           0.0     15.0
# 25%           0.1    119.4
# 50%           0.1    180.4
# 75%           0.2    265.0
# max           1.9    500.0

# 可视化
sample = california_housing_dataframe.sample(n=300)
x_0 = sample['total_rooms'].min()
x_1 = sample['total_rooms'].max()
weight = linear_regressor.get_variable_value('linear/linear_model/total_rooms/weights')[0]
bias = linear_regressor.get_variable_value('linear/linear_model/bias_weights')
y_0 = weight * x_0 + bias
y_1 = weight * x_1 + bias
plt.plot([x_0,x_1],[y_0, y_1], c='r')
plt.xlabel('total_rooms')
plt.ylabel('median_house_value')
plt.scatter(sample['total_rooms'], sample['median_house_value'])
plt.show()
'''
