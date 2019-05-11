#!/usr/bin/env python3
import datetime
import pandas as pd
from datetime import datetime
import json
import os
import codecs
import numpy as np
import traceback
import sys
import gensim
#from gensimplus.source.gensim_plus_config import FLAGS
#from gensimplus.source.model_save_load_helper import ModelSaveLoadHelper
from gensim.models import LsiModel
from gensim.models import LdaModel
from gensim.models import TfidfModel
import jieba
import jieba.posseg
import user_prob
from user_prob.test import new_cut
import re
import numpy as np
import pdb
import codecs
import trie_tree
import utils
#DEBUG = False
CURPATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append("../..")
sys.path.append("..")
sys.path.append(".")
sys.path.append(os.path.join("..",CURPATH))
DICT = False#$True
DEBUG = True
JIEBACUT= True
global r_cnt
global w_cnt
r_cnt = 1
w_cnt = 0
standard_addr = {}

load_json = lambda x:json.load(open(x,'r',encoding='utf-8'))

standard_addr = load_json(os.path.join(CURPATH,"standard_addr.json"))

standard_dct = {}
ks = []
vs = []

for item in standard_addr['RECORDS']:
    v = item['name']
    k = item['type']
    ks.append(k)
    vs.append(v)

keys = list(set(ks))
values = list(set(vs))

level_keys = ["省","市","区","社区","村居委会","街路巷名","自然村组",\
              "门牌号","小区名","建筑物名称","组团名称","栋号",\
              "单元号","楼层","户室号","sent","rw"]

out_keys = ["省","市","区","社区","村居委会","街路巷名","自然村组","门牌号","小区名","组团名称","栋号","单元号","楼层","户室号"]

global global_cnt

def read_standard_data(self,docpath='standard_address.json'):
    '''
    read word from standard dict, return key words dict 
    '''
    standard_kvs = {}
    standard_num = {}
    fl = open(docpath,'r',encoding='utf-8')
    info = json.load(fl)
    return info #返回标准地址库
    kvs_lst = info.get('RECORDS','')
    for item in kvs_lst:
        k = item.get('name','')
        v = len(standard_kvs)
        standard_kvs[k] = v
    for k in standard_kvs:
        _k = standard_kvs[k]
        _v = k
        standard_num[_k] = _v
    return standard_kvs, standard_num

def gen_address_tree(filename='/home/distdev/src/iba/dmp/gongan/gy_addr_normal/pre_data/yyap_address_tree.csv',sav_file='./my_tree.pkl'):
    print('\n>gen_address_tree start')
    my_tree = trie_tree.Trie()
    df = pd.read_csv(filename)
    for idx in df.index.values:
        sent = df.iloc[idx,1]
        words = sent.split('/')
        my_tree.insert(words)
    utils.save_var(my_tree,sav_file)
    print('\n>my address tree save ok')

def load_address_tree(sav_file='./my_tree.pkl'):
    my_tree = utils.read_var(sav_file)
    return my_tree

#gen_address_tree()   

if __name__ == "__time__":
    pass
    print('') 
    gen_address_tree(filename='/home/distdev/src/iba/dmp/gongan/gy_addr_normal/pre_data/yyap_address_tree.csv',sav_file='./my_tree.pkl')
