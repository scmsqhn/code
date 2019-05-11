#!/usr/bin/env python3
import datetime
import time
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
import struct
from function_ultra import *
from struct_ultra import *
from business_ultra import *
import numpy as np
import pandas as pd
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
import myconfig

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
import business_ultra.init_data as init_data

class ActiMatch(object):

    def __init__(self,pkl_path):
        self.addr_tree = init_data.load_address_tree(pkl_path.get('std_tree'))
        self.word_tree = init_data.load_address_tree(pkl_path.get('word_tree'))
        #self.addr_tree = init_data.load_address_tree("shequ_sample_tree.pkl")
        #self.ks = ["小区名","单元号","楼层",'户室号']
        self.ks = ["区","街路巷名","门牌号","栋号","单元号","楼层"]
        #self.ks = ["区","社区","村居委会","街路巷名","自然村组","门牌号","小区名","组团名称","栋号","单元号","楼层","户室号"]
        self.ks_1 = ["区","社区","村居委会","街路巷名","自然村组"]
        self.ks_1 = self.ks_1[::-1]
        self.ks_2 = ["栋号","单元号","楼层","户室号"]
        print('\n>ActiMatch init')

    def search(self,tree,words):
        '''
        key func: to search the words
        words:dict
        '''
        t0 = time.time()
        res = tree.scan_word([tree.root],words)
        t1 = time.time()
        print(t1-t0)
        return res

    def data_clr(self,item):
        levels = ['栋号','单元号','楼层','户室号']
        level_words = ['栋','单元','层','']
        result = []
        for key,word in zip(levels,level_words):
            item = self.rep(item,key,word)
        for k in self.ks: 
            if not item.get(k,'') == '':
                result.append(item.get(k))
        return result,item.get('sent','')
            
    def rep(self,item,key,value):
        '''
        format one place in dict
        '''
        if not item.get(key,'') == '':
            cont = item.get(key,'')
            cont = re.sub('[\u4e00-\u9fa5]','',cont)
            cont+=value
            item[key] = cont
        return item
        
    def stand_data_gen(self, input_file):
        df = pd.read_csv(input_file)
        addrs = df.iloc[:,1]
        for addr in addrs:
            #addr = utils.pre_trans(addr)
            words = addr.split('/')
            _words = []
            if '层' in words[-2]:
                words[-1]+="室"
            for word in words[5:]:
                if '组团' in word:
                    pass
                if '期' in word:
                    pass
                _words.append(word)
            yield _words
            
    def read_file(self,input_file):
        lines = open(input_file,"r").readlines()
        for line in lines:
            line = re.sub('[- ]','',line)
            yield line
        
    def data_gen(self,input_file):
        lines = open(input_file,"r").readlines()
        dct = {}
        item = {}
        for line in lines:
            if 'NEXT' in line:
                words,sent = self.data_clr(item)
                item = {}
                yield words,sent
            else:
                k,v = line.split('\t')
                if len(k)>0 and len(v)>0:
                   k,v = re.sub("[ \n]","",k), re.sub("[ \n]","",v)
                   item[k] = v

    def mode_match(self, sentence,lth=7):
        '''
        func: filter word in standard lib
        sentence: sentence
        '''
        res = []
        res = self.word_tree.mode_match(sentence, res, lth=7)
        return res

    def filter(self, words):
        res = []
        for word in words:
            if len(re.findall('\d+',word))>0:
                if len(res) == 0:
                    res.append(words[words.index(word)-1])
                res.append(word)
                if len(res) >2:
                   return res
        return res

if __name__ == '__main__':
    import sys
    import business_ultra.reghelper as reghelper
    reg = reghelper.RegHelper()
    '''
    加载所有样本地址，所有节点信息
    '''
    #init_data.gen_zhengzhou_tree()
    kv = {}
    print('\n>load tree std word')
    kv['word_tree'] = myconfig.zhengzhou_std_word
    print('\n>load tree std tree')
    kv['std_tree'] = myconfig.zhengzhou_std_tree
    print('\n>load tree finish')
    acti_match_ins = ActiMatch(kv)
    '''
    生成地址树
    '''
    f = open('郑州比对程序测试.txt','a+')
    _filename = "/data/corpmgr/区域语料/郑州/zz_std_words.txt"
    #_filename = "/data/corpmgr/区域语料/郑州/dz_zzxx_cs.2.txt"
    gen = acti_match_ins.read_file(_filename)
    reqs = set()
    fail_cnt = 0
    while(fail_cnti<100000):
        item = gen.__next__()
        #print(item)
        #item = re.sub('"(.+?)","(.+?)"',"\\2",item)
        #print(item)
        item = utils.pre_trans(item)
        kvs = reg.address_formula(item)
        
        std_lst = []
        std_words = []
        std_words.append(kvs.get('街路巷名',''))
        _d = re.sub('\D','',kvs.get('门牌号',''))
        std_words.append(_d)
        _d = re.sub('\D','',kvs.get('栋号',''))
        std_words.append(_d)
        std_lst.append(std_words)

        std_words = []
        std_words.append(kvs.get('小区名',''))
        _d = re.sub('\D','',kvs.get('栋号',''))
        std_words.append(_d)
        std_lst.append(std_words)

        std_words = []
        _d = re.sub('\D','',kvs.get('组团名称',''))
        std_words.append(_d)
        _d = re.sub('\D','',kvs.get('栋号',''))
        std_words.append(_d)
        std_lst.append(std_words)

        #std_words = []
        #std_words.append(kvs.get('建筑物名称',''))
        #std_lst.append(std_words)

        std_words = []
        std_words.append(kvs.get('小区名',''))
        std_lst.append(std_words)

        std_words = []
        _d = re.sub('\D','',kvs.get('组团名称',''))
        std_words.append(_d)
        std_lst.append(std_words)

        '''
        比例
        '''
        #print(item)
        #if len(item) == 0:
        #    continue
        res = []
        print('\n> 原有输入句子: %s'%item)
        #words = acti_match_ins.word_tree.mode_match(item,res,lth=7)
        #words = acti_match_ins.filter(words)
        #res = acti_match_ins.search(acti_match_ins.addr_tree,'河')
        #print(res)
        #res = acti_match_ins.search(acti_match_ins.word_tree,'河')
        #print(res)
        for wds in std_lst:
            if '' in wds:
                continue
            wds = ''.join(wds)
            if wds in reqs:
                fail_cnt+=1
                print('fail_cnt: ',fail_cnt)
                continue
            fail_cnt = 0
            reqs.add(wds)
            print('\n> 在地址树中检索: ', wds)
            '''
            考虑到wds里面有'',代表有相关的地址没有，避免检索弄错，将这个词条丢弃
            '''
            res = acti_match_ins.search(acti_match_ins.addr_tree, wds)
            _res = acti_match_ins.search(acti_match_ins.word_tree, wds)
            res.extend(_res)
            res = list(set(res))
            if len(res)>0:
                print('\n> 检索结果 : %s'%res)
            for resitem in res:
                f.write("%s,%s\n"%(item,resitem))
            f.flush()

