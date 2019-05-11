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
sys.path.append(os.environ['YUNYAN'])
sys.path.append(os.environ['ROOT'])
sys.path.append(os.environ['WORKBENCH'])
#import gensim
#from gensimplus.source.gensim_plus_config import FLAGS
#from gensimplus.source.model_save_load_helper import ModelSaveLoadHelper
#from gensim.models import LsiModel
#from gensim.models import LdaModel
#from gensim.models import TfidfModel
import myconfig
import src
from src import myjieba_posseg
from myjieba_posseg import posseg as posseg
import user_prob
from user_prob.test import new_cut
import re
import numpy as np
import pdb
import codecs
import function_ultra.trie_tree as trie_tree
import function_ultra.utils as utils
#DEBUG = False
DICT = False#$True
DEBUG = True
JIEBACUT= True
global r_cnt
global w_cnt
r_cnt = 1
w_cnt = 0
standard_addr = {}
load_json = lambda x:json.load(open(x,'r',encoding='utf-8'))

standard_addr = load_json(myconfig.STDADD)

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

def gen_word_tree(filename=myconfig.STDTXTPATH,sav_file=myconfig.MY_WORD):
    print('\n>gen_address_tree start')
    my_tree = trie_tree.Trie()
    df = open(filename,'r')
    lines = df.readlines() #pd.read_csv(filename)
    print(len(lines))
    for sent in lines:
        words = sent.split('/')
        for word in words:
            my_tree.insert(word)
    utils.save_var(my_tree,sav_file)
    print('\n>my address tree save ok')
    return my_tree

def gen_std_tree(filename=myconfig.STDTXTPATH,sav_file=myconfig.MY_TREE,delimeter='/'):
    print('\n>gen_std_tree start')
    my_tree = trie_tree.Trie()
    df = open(filename,'r')
    lines = df.readlines() #pd.read_csv(filename)
    for sent in lines:
        words = sent.split(delimeter)
        my_tree.insert(words)
    utils.save_var(my_tree,sav_file)
    print('\n>my std tree save ok')
    return my_tree

def remove_nan(item):
    clritem = []
    for node in item:
        if 'nan' in node:
            continue
        clritem.append(node)
    return clritem

def gen_std_tree_from_dataframe(data_src, sav_file=myconfig.MY_TREE):
    # 从dataframe创建标准地址树
    print('\n>gen_std_tree_from_dataframe start')
    my_tree = trie_tree.Trie()
    for item in data_src:
        clritem = remove_nan(item)
        print(clritem)
        pdb.set_trace()
        my_tree.part_insert(my_tree.root,clritem)
    utils.save_var(my_tree,sav_file)
    print('\n>gen_std_tree_from_dataframe ready and save finish')
    return myconfig.SUCCESS

def gen_address_tree(filename=myconfig.STDTXTPATH,sav_file=myconfig.MY_TREE):
    print('\n>gen_address_tree start')
    my_tree = trie_tree.Trie()
    df = open(filename,'r')
    lines = df.readlines() #pd.read_csv(filename)
    for sent in lines:
        my_tree.insert(sent)
    utils.save_var(my_tree,sav_file)
    print('\n>my address tree save ok')
    return my_tree

def gen_zhengzhou_tree(dirname=myconfig.ZZ_STD_ADD,sav_file=myconfig.zhengzhou_std_word,sav_file_2=myconfig.zhengzhou_std_tree):
    addr_kv_rec = open("./addr_match.txt",'w+')
    print('\n>gen_zhengzhou_tree start')
    #pdb.set_trace()
    my_tree = trie_tree.Trie()
    my_word = trie_tree.Trie()
    paths = os.walk(dirname)
    sum_lines = []
    cnt = 0
    for _,_,fs in paths:
        for f in fs:
            pth = os.path.join(dirname,str(f))
            lines = open(pth,'r').readlines()
            np.random.shuffle(lines)
            #lines = open(pth,'r').readlines()[:myconfig.TRAIN_DATA]
            for line in lines:
                if not ',' in line:
                    continue
                _line = line.split(',')[1]
                line = utils.pre_trans(_line)
                addr_kv_rec.write('%s\t%s\n'%(str(line),str(_line)))
                cnt+=1
                if cnt%10000==1:
                    print(cnt)
                my_tree.insert(line)
                my_word.insert(_line)
    utils.save_var(my_word,sav_file)
    utils.save_var(my_tree,sav_file_2)
    print('\n>my address tree save ok')
    addr_kv_rec.close()

def load_address_tree(sav_file='./my_tree.pkl'):
    my_tree = utils.read_var(sav_file)
    return my_tree

#gen_address_tree()

if __name__ == "__time__":
    pass
    print('')
    gen_address_tree(filename='/home/distdev/src/iba/dmp/gongan/gy_addr_normal/pre_data/yyap_address_tree.csv',sav_file='./my_tree.pkl')
