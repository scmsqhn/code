# coding: utf-8

'''
思想
使用adabooster回归树对于,地址中的序列信息进行分类
实现成本低,可以快速迭代,验证所找的特征
验证成功后,使用深度学习模型代替
可以解决,用户需求多变的问题
目前积累的回归树有
街道匹配回归判断
楼号匹配回归判断
'''

import os
import pdb
import re
import sys

from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score

import numpy as np
from utils import *
import xgboost as xgb


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

CHAR_HASH_DIVIDE = 3000
LENTH_PADDING = 15
TRAIN_DATA = 1000000
EVAL_DATA = 300
HASH_MAX = 77777777
CHECK_RULE_JIEDAO = re.compile("\D\D\D[街道路巷村镇坡屯]")
CHECK_RULE_LOUHAO = re.compile(
    "([一二三四五六七八九零]+?[号杠])(?:.*?)?([一二三四五六七八九零]+?[号杠$])")

leval_name_list = ['省', '市', '区', '社区', '村居委会', '自然村组',
                   '街路巷名', '小区名', '门牌号', '组团名称',
                   '建筑物名称', '楼号', '楼层', '栋号', '单元号', '户室号']
level_name2key = dict()
level_key2name = dict()
for i, name in enumerate(leval_name_list):
    level_name2key[name] = i
    level_key2name[i] = name


def trans(chars):
    DIV = CHAR_HASH_DIVIDE  # 3000
    size = LENTH_PADDING    # 15
    padding = []
    for char in chars:
        char_num = ord(str(char))
        char_num = char_num % DIV
        padding.append(char_num)
    if not (len(padding) - size >= 0):
        padding.extend([ord(" ") % DIV] * size)
    return padding[:size]


def shequ_jingqu_quanliang_shuju_data_gen(stdfile, cnt=1000000, shuffle=True):
    lines = open(stdfile, "r").readlines()
    X_train, y_train = [], []
    last_word = ""
    for line in lines:
        cnt -= 1
        if cnt < 0:
            break
        if shuffle:
            line = lines[np.random.randint(len(lines))]
        if not "\t" in line:
            continue
        if "sent" in line:
            continue
        if "rw" in line:
            continue
        if 'START' in line:
            last_word = ""
            continue
        try:
            assert len(line.split("\t")) == 2
        except AssertionError:
            continue
        line = re.sub(" ", "", line)
        k, v = line.split("\t")
        X_train.append(trans(last_word + v))
        y_train.append(level_name2key[k])
        last_word = v
    d_train = xgb.DMatrix(np.array(
        X_train).reshape(-1, LENTH_PADDING), label=np.array(y_train).reshape(-1))
    return d_train, y_train


def xgb_train(dtrain, num_round=4):
    params = {
        'booster': 'gbtree',
        'objective': 'multi:softmax',  # 多分类的问题
        'num_class': len(leval_name_list),  # 类别数，与 multisoftmax 并用
        'gamma': 0.1,                  # 用于控制是否后剪枝的参数,越大越保守，一般0.1、0.2这样子。
        'max_depth': 12,               # 构建树的深度，越大越容易过拟合
        'lambda': 2,                   # 控制模型复杂度的权重值的L2正则化项参数，参数越大，模型越不容易过拟合。
        'subsample': 0.7,              # 随机采样训练样本
        'colsample_bytree': 0.7,       # 生成树时进行的列采样
        'min_child_weight': 3,
        'silent': 1,                   # 设置成1则没有运行信息输出，最好是设置为0.
        'eta': 0.007,                  # 如同学习率
        'seed': 1000,
        'nthread': 4,                  # cpu 线程数
    }

    bst = xgb.train(params, dtrain, num_round)
    return bst


def _train(std_file=u"/home/phoenixkiller/nlppipeline/shequ", model=os.path.join(DATA_DIR, 'classifier.model')):
    dtrain, y_train = shequ_jingqu_quanliang_shuju_data_gen(
        std_file, cnt=TRAIN_DATA, shuffle=True)
    bst = xgb_train(dtrain, num_round=100)
    bst.save_model(model)
    dtest, y_test = shequ_jingqu_quanliang_shuju_data_gen(
        std_file, cnt=TRAIN_DATA, shuffle=True)
    pred = bst.predict(dtest)
    print(pred, y_test)
    print(accuracy_score(pred, y_test))
    print(recall_score(pred, y_test, average='macro'))


def _pred(k, v, bst):
    X_train, y_train = [], []
    X_train.append(trans(v))
    y_train.append(level_name2key[k])
    d_pred = xgb.DMatrix(np.array(
        X_train).reshape(-1, LENTH_PADDING), label=np.array(y_train).reshape(-1))
    pred = bst.predict(d_pred)
    print(pred, k, v)
    return level_key2name[pred[0]]


if __name__ == "__main__":
    std_file = os.path.join(DATA_DIR, "train_classifier.txt")
    if sys.argv[1] == "train":
        _train(std_file, os.path.join(DATA_DIR, "classifier.model"))
    elif sys.argv[1] == "valid":
        dtest, y_test = shequ_jingqu_quanliang_shuju_data_gen(
            std_file, cnt=TRAIN_DATA, shuffle=True)
        bst = xgb.Booster()  # init model
        bst.load_model(os.path.join(DATA_DIR, "classifier.model"))
        pred = bst.predict(dtest)
        print(pred, y_test)
        print(accuracy_score(pred, y_test))
        print(recall_score(pred, y_test, average='macro'))
        for i, j in zip(pred, y_test):
            if not i == j:
                print(i, j, "not equal")
    else:
        bst = xgb.Booster()  # init model
        bst.load_model(os.path.join(DATA_DIR, "classifier.model"))
        print(_pred("省", "青羊区", bst))
