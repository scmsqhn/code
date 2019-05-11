#!/usr/bin/python
# -*- coding: utf-8 -*-
import pdb
import numpy as np
import os
import sys
sys.path.append('.')
sys.path.append('./business_ultra')
import myconfig
sys.path.append(myconfig.PRJPATH)
sys.path.append(myconfig.SRCPATH)
from sklearn.externals.six.moves import zip
import matplotlib.pyplot as plt
from sklearn.datasets import make_gaussian_quantiles
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib
import function_ultra
import function_ultra.utils as utils
import function_ultra.mark_train_data as mark_train_data
from mark_train_data import hugry_match, matrix_build
from utils import *
import sys
sys.path.append(".")
sys.path.append("/data/guizhou_address/address_formula_release/src")
sys.path.append("/data/guizhou_address/address_formula_release")
sys.path.append("/data/guizhou_address")
sys.path.append("..")
sys.path.append(".")
import address_formula_release.src.reghelper

# 载入数据
import mylog
from mylog import logger as logger
logger.debug("start")
import xgboost as xgb
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score

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
test1 = "12号楼9单元1号"
test2 = "20单元10单元1号"
lbl = 0

def calc(cbase,csent):
    logger.debug("%s %s"%(cbase,csent))
    data,label,s,r,c = hugry_match(matrix_build(cbase,csent,weight=0),cbase,csent)
    _,_,sa,_,_ = hugry_match(matrix_build(cbase,csent,weight=1),cbase,csent)
    _,_,sp,_,_ = hugry_match(matrix_build(cbase,csent,weight=-1),cbase,csent)
    d = utils.minEditDist(cbase,csent)
    hamming = 0
    for i,j in zip(r,c):
        if cbase[i]==csent[j]:
            continue
        hamming+=1
    return hamming,s,sa,sp,d,r,c,data,label

def rule_check(src,tar,rule="louhao"):
    src = utils.clr(src)
    tar = utils.clr(tar)
    logger.debug("%s %s\n"%(src, tar))
    if rule == "louhao":
        #reg0 = re.compile("([一二三四五六七八九零]+?[号杠])(?:.*?)?([一二三四五六七八九零]+?[号杠$])")
        reg0 = myconfig.CHECK_RULE_LOUHAO
        src0 = re.findall(reg0,src)
        tar0 = re.findall(reg0,tar)
        if len(src0)>0:
            src0 = "".join(src0[0])
        else:
            src0 = ""
        if len(tar0)>0:
            tar0 = "".join(tar0[0])
        else:
            tar0 = ""
        print(src0, tar0, src, tar)
        if src0 == tar0 and not src0 =="":
            return True
        else:
            return False
    elif rule == "jieluxiang":
        #======
        #reg0 = re.compile("\D\D\D[街道路巷]")
        reg0 = myconfig.CHECK_RULE_JIEDAO
        src0 = re.findall(reg0,src)
        tar0 = re.findall(reg0,tar)
        if len(src0)>0 and len(tar0)>0:
            if src0[-1] == tar0[-1]:
                return True
        return False
    else:
        print(rule)

def rule_lst_check(line1,line2,rules):
    '''
    检查多个规则是否可行
    '''
    result = []
    for rule in rules:
        if rule_check(line1,line2,rule):
            result.append(True)
        else:
            result.append(False)
    if False in result:
        return False
    return True

def data_gen(stdfile,cnt,shuffle=False,rule='jieluxiang'):
    if cnt==-1:
        cnt=10e+30
    X_train = []
    y_train = []
    lines_std = open(stdfile,"r").readlines()
    for line in lines_std:
        '''
        是否需要把不符合条件的删除掉
        '''
        if shuffle:
            line = lines_std[np.random.randint(len(lines_std))]
        line1 = ""
        line2 = ""
        lb = True
        if "ROOT" in line:
            line1,line2 = line.split("ROOT")
            lb = rule_check(line1,line2,rule=rule)
        elif "NONE" in line:
            line1,line2 = line.split("NONE")
            lb = rule_check(line1,line2,rule=rule)
        else:
            continue
        train_data_piece = get_data(line1,line2,rule)
        X_train.append(train_data_piece)
        #lb = rule_lst_check(line1,line2,rules)
        y_train.append(lb)
        cnt-=1
        if cnt<0:
            return np.concatenate(tuple(X_train),axis=0), np.array(y_train).reshape(-1,1)
    return np.concatenate(tuple(X_train),axis=0), np.array(y_train).reshape(-1,1)

def hamming(src,dat):
    cnt = 0
    for i,j in zip(src,dat):
        if not i == j:
            cnt+=1
    return cnt

def get_xgb_data(src, tar, direct):
    #讲文本对齐padding后返回
    if direct == "char":
        src = utils.char_filter(src)
        tar = utils.char_filter(tar)
        logger.debug("%s %s\n"%(src, tar))
        src,tar = utils.padding(src,tar,direct="ahead")
        return src,tar
    elif direct == "num":
        src = utils.num_filter(src)
        tar = utils.num_filter(tar)
        logger.debug("%s %s\n"%(src, tar))
        src,tar = utils.padding(src,tar,direct="ahead")
        return src,tar
    elif direct == "jieluxiang":
        src = utils.jieluxiang_filter(src)
        tar = utils.jieluxiang_filter(tar)
        logger.debug("%s %s\n"%(src, tar))
        src,tar = utils.padding(src,tar,direct="ahead")
        return src,tar
    else:
        logger.debug("get_xg_data,there must be sth wrong")

def padding(lst,l0=15,dummy=-1):
    result= []
    for i in range(l0):
        if i < len(lst):
            result.append(lst[i])
        else:
            result.append(dummy)
    return result

def mode_match_str(src,tar):
    char_and = set(src) & set(tar)
    indexa,indexb = [],[]
    for char in char_and:
        indexa.append(src.index(char))
        indexb.append(tar.index(char))
    print(sorted(indexa), sorted(indexb))
    return sorted(indexa), sorted(indexb)

def get_data(src,tar,direct):
    #把文本映射到可以用来泛化的向量空间，手动映射，向量空间包括二部图匹配，开销矩阵，编辑距离，汉明距离等
    result = []
    #对齐，前部填充后，返回
    src,tar = get_xgb_data(src, tar, direct)
    print(src,tar)
    #对齐，前部填充后，返回
    hamming,s,sa,sp,d,r,c,data,label = calc(src,tar)
    result.extend([hamming,s,sa,sp,d])
    result.extend(padding(r))
    result.extend(padding(c))
    result.extend(padding(label))
    hamming,s,sa,sp,d,r,c,data,label = calc(tar,src)
    result.extend([hamming,s,sa,sp,d])
    result.extend(padding(r))
    result.extend(padding(c))
    result.extend(padding(label))
    #match_pre,match_aft = mode_match_str(src,tar)
    #result.extend(padding(match_pre))
    #result.extend(padding(match_aft))
    #双向匹配后输出
    import myconfig
    LEN = myconfig.CHAR_HASH_DIVIDE
    codes = []
    for char in src:
        code = ord(char)%LEN
        codes.append(code)
    result.extend(padding(codes))
    codes = []
    for char in tar:
        code = ord(char)%LEN
        codes.append(code)
    result.extend(padding(codes))
    return np.array(result).reshape(-1,len(result))

def load_model(model_name):
    bst_new = xgb.Booster() #init model
    bst_new.load_model(model_name) # load data
    return bst_new

def sav_model(bst,model_name):
    bst.save_model(model_name)
    logger.debug("xgboost mode save ok")
    return 0

from sklearn.metrics import confusion_matrix
def fscore(preds, dtrain):
     label = dtrain.get_label()
     pred = [int(i>=0.5) for i in preds]
     confusion_matrixs = confusion_matrix(label, pred)
     recall =float(confusion_matrixs[0][0]) / float(confusion_matrixs[0][1]+confusion_matrixs[0][0])
     precision = float(confusion_matrixs[0][0]) / float(confusion_matrixs[1][0]+confusion_matrixs[0][0])
     F = 5*precision* recall/(2*precision+3*recall)*100
     return float(F)

def xgb_train(dtrain,num_round=4):
    #param = {'max_depth':3, 'eta':1, 'silent':0, 'objective':'binary:logistic',\
    #         'lambda':1, 'alpha' :1, 'scale_pos_weight':3, 'feval':fscore}
    #param = {'objective':'multi:softmax','num_class':len(global_dct)}
    params = {
    'booster': 'gbtree',
    'objective': 'multi:softmax',  # 多分类的问题
    'num_class': len(global_dct),               # 类别数，与 multisoftmax 并用
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

def trans(chars):
    DIV = myconfig.CHAR_HASH_DIVIDE
    size = myconfig.LENTH_PADDING
    padding = []
    for index in range(len(chars)):
        char = chars[index]
        char_num = ord(str(char))
        char_num = char_num%DIV
        padding.append(char_num)
        print(char,char_num)
    if not len(padding)-size>=0:
        padding.extend([ord(" ")%DIV]*size)
    print(padding[:size])
    return padding[:size]

def init_global_cnt():
    global_dct = {\
    '省': 0, \
    '市': 1, \
    '区': 2, \
    '社区': 3, \
    '村居委会': 4, \
    '自然村组': 5, \
    '街路巷名': 6,\
    '小区名': 7, \
    '门牌号': 8, \
    '组团名称': 9, \
    '建筑物名称': 10, \
    '楼号': 11, \
    '楼层': 12, \
    '栋号': 13, \
    '单元号':14, \
    '户室号': 15, \
    '其他': 15, \
    }
    global_num_dct = {}
    for k in global_dct:
        global_num_dct[global_dct[k]] = k
    return global_dct, global_num_dct

global_dct,global_num_dct = init_global_cnt()

'''
def dct_trans(k,dct):
    if k in dct:
        return dct[k]
    else:
        dct[k] = len(dct)
        return dct[k]
'''

def dct_trans(k,global_dct):
    res = global_dct.get(k,'其他')
    return res

def xgboost_train_data_gen(cnt=myconfig.TRAIN_DATA,shuffle=True):
    X_train,y_train = [],[]
    gen = os.walk("../address_gy/source/dct_file/dct_level")
    for path,_,files in gen:
        for filename in files:
            if filename == "tokens.txt":
                continue
            lines = open(os.path.join(path,filename),"r").readlines()
            for line in lines:
                if not k in dct_trans:
                    continue
                line = utils.clr(line)
                X_train.append(trans(line))
                filename = filename.split(".")[0]
                y_train.append(dct_trans(filename,global_dct))
    #print(len(lines))
    d_train = xgb.DMatrix(np.array(X_train).reshape(-1,myconfig.LENTH_PADDING), label=np.array(y_train).reshape(-1))
    return d_train,y_train
        
def _train(std_file=u"/home/phoenixkiller/nlppipeline/shequ",model='classifier.model'):
    #X_train,y_train = data_gen(std_file,cnt=myconfig.TRAIN_DATA,shuffle=True,rule='jieluxiang')
    dtrain,y_train = shequ_jingqu_quanliang_shuju_data_gen(std_file,cnt=myconfig.TRAIN_DATA,shuffle=True)
    print('#' * 50)
    print(dtrain[:3])
    print(y_train[:3])
    bst = xgb_train(dtrain,num_round=100)
    result = sav_model(bst,model)
    #X_test,y_test = data_gen(std_file,cnt=100,shuffle=True,rule='jieluxiang')
    dtest,y_test = shequ_jingqu_quanliang_shuju_data_gen(std_file,cnt=myconfig.TRAIN_DATA,shuffle=True)
    pred = bst.predict(dtest)
    #pred = [True if i>0.5 else False for i in pred]
    print(pred,y_test)
    print(accuracy_score(pred, y_test))
    print(recall_score(pred, y_test, average='macro'))

def shequ_jingqu_quanliang_shuju_data_gen(reg,stdfile,cnt=myconfig.TRAIN_DATA,shuffle=True):
    lines = open(stdfile,"r").readlines()
    X_train,y_train = [],[]
    last_word = ""
    for line in lines:
        cnt-=1
        if cnt < 0:
            break
        if shuffle:
            _line = lines[np.random.randint(len(lines))]
            kvs = reg.address_formula(_line)
            vs = [kvs[k] for k in kvs]
            others = re.split(_line,str(vs))
            for k in kvs:
                if not k in global_dct:
                    continue
                X_train.append(trans(kvs[k]))
                y_train.append(dct_trans(k,global_dct))
            for wd in others:
                X_train.append(trans(wd))
                y_train.append(dct_trans('其他',global_dct))
    pdb.set_trace()
    d_train = xgb.DMatrix(np.array(X_train).reshape(-1,myconfig.LENTH_PADDING), label=np.array(y_train).reshape(-1))
    return d_train,y_train
        
def _train(std_file=u"/home/phoenixkiller/nlppipeline/shequ",reg='',model='classifier.model'):
    #X_train,y_train = data_gen(std_file,cnt=myconfig.TRAIN_DATA,shuffle=True,rule='jieluxiang')
    #dtrain,y_train = xgboost_train_data_gen(cnt=myconfig.TRAIN_DATA, shuffle=True)
    dtrain,y_train = shequ_jingqu_quanliang_shuju_data_gen(reg,std_file,cnt=myconfig.TRAIN_DATA,shuffle=True)
    #print('#' * 50)
    #print(dtrain[:3])
    #print(y_train[:3])
    bst = xgb_train(dtrain,num_round=100)
    result = sav_model(bst,model)
    #X_test,y_test = data_gen(std_file,cnt=100,shuffle=True,rule='jieluxiang')
    dtest,y_test = shequ_jingqu_quanliang_shuju_data_gen(reg,std_file,cnt=myconfig.EVAL_DATA,shuffle=True)
    pred = bst.predict(dtest)
    #pred = [True if i>0.5 else False for i in pred]
    print(pred,y_test)
    print(accuracy_score(pred, y_test))
    print(recall_score(pred, y_test, average='macro'))
    pdb.set_trace()

def _eval(std_file=u"/home/phoenixkiller/nlppipeline/ONSELL.txt.POSNEG",model='classifier.model'):
    #X_test,y_test = data_gen(std_file,cnt=myconfig.EVAL_DATA,shuffle=True,rule='jieluxiang')
    dtest,y_test = shequ_jingqu_quanliang_shuju_data_gen(reg,std_file,cnt=myconfig.EVAL_DATA,shuffle=True)
    bst = load_model(model)
    pred = bst.predict(dtest)
    #pred = [True if i>0.5 else False for i in pred]
    print(pred,y_test)
    print(accuracy_score(pred, y_test))
    print(recall_score(pred, y_test, average='macro'))
    pdb.set_trace()
    for i,j in zip(pred,y_test):
        if not i == j:
            print(i,j,"not equal")

def _pred(k,v,bst):
    X_train, y_train = [],[]
    X_train.append(trans(v))
    y_train.append(dct_trans(k,global_dct))
    d_pred = xgb.DMatrix(np.array(X_train).reshape(-1,myconfig.LENTH_PADDING), label=np.array(y_train).reshape(-1))
    pred = bst.predict(d_pred)
    print(pred,k,v)
    return global_num_dct[pred[0]]

if __name__ == "__main__":
    #std_file = u"/home/phoenixkiller/nlppipeline/ONSELL.txt.POSNEG"
    reg = address_formula_release.src.reghelper.RegHelper()
    std_file = "/data/社区警务全量地址.txt"
    eval_file = "/data/常口户籍数据.txt"
    #std_file = "/data/address_gy/source/train_classifier.txt"
    _train(std_file,reg,"classifier.model")
    #pdb.set_trace()
    #_eval(eval_file,"classifier.model")
    #pdb.set_trace()
    bst = load_model("classifier.model")
    print(_pred("省","青羊区",bst))
    print(_pred("省","光明街居委会",bst))
    print(_pred("省","中坝",bst))
    print(_pred("省","太原市",bst))
    print(_pred("省","天府广场",bst))
    print(_pred("省","南泥湾",bst))
    print(_pred("省","万达城",bst))
