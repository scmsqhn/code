#!/usr/bin/env python3
import datetime
import time
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
sys.path.append("../..")
import myconfig
import myjieba_posseg
import myjieba_posseg.posseg as posseg
#from myjieba import posseg
import user_prob
#from user_prob.test import new_cut
import re
import numpy as np
import pdb
import codecs
#DEBUG = False
CURPATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join("..",CURPATH))
import function_ultra
from function_ultra import utils
from function_ultra import network_app
DICT = False#$True
DEBUG = True
JIEBACUT= True
global r_cnt
global w_cnt
r_cnt = 1
w_cnt = 0
standard_addr = {}

load_json = lambda x:json.load(open(x,'r',encoding='utf-8'))

standard_addr = load_json(myconfig.pth("data/standard_addr.json"))

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
sys.path.append(CURPATH)

sys.path.append(CURPATH)

import function_ultra
import business_ultra
from business_ultra import init_data


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton

@Singleton
class ActiMatch(object):

    def __init__(self,s):
        #self.addr_tree = init_data.gen_address_tree()
        self.addr_tree = init_data.load_address_tree(sav_file=myconfig.MY_TREE)
        self.m_network_app = network_app.networkx_app()
        #self.word_tree = init_data.gen_word_tree()
        #kv = {}
        #kv['word_tree'] = 'word_tree.pkl'
        #kv['addr_tree'] = 'addr_tree.pkl'
        #self.kv = kv
        #self.ks = ["区","街路巷名","门牌号","栋号","单元号","楼层"]
        #self.ks_1 = ["区","社区","村居委会","街路巷名","自然村组"]
        #self.ks_1 = self.ks_1[::-1]
        #self.ks_2 = ["栋号","单元号","楼层","户室号"]
        #self.ks = ["区","社区","村居委会","街路巷名","自然村组","门牌号","小区名","组团名称","栋号","单元号","楼层","户室号"]

    def search(self,words):
        if words == 'CMDDCT':
            self.addr_tree = init_data.load_address_tree(sav_file=myconfig.MY_TREE)
            #self.addr_tree = init_data.gen_std_tree()
            #self.word_tree = init_data.gen_word_tree()
            return ['CMDDCT FINISH']
        '''
        key func: to search the words
        words:dict
        '''
        words = re.sub("[^ ]+?/[a-z]+? ","",words)
        res = self.m_network_app.search(words)
        return res

    def full_search(self,words):
        if words == 'CMDDCT':
            self.addr_tree = init_data.load_address_tree(sav_file=myconfig.MY_TREE)
            #self.addr_tree = init_data.gen_std_tree()
            #self.word_tree = init_data.gen_word_tree()
            return ['CMDDCT FINISH']
        '''
        key func: to search the words
        words:dict
        '''
        words = words.split(' ')
        if '' in words:
            words.remove('')
        zhuzhai = []
        cunzhuang = []
        jianzhu = []
        print(words)
        search_dct = {}
        for word in words:
            if 'nan' in word:
                continue
            if 'DIST' in word:
                zhuzhai.append(word)
                cunzhuang.append(word)
                jianzhu.append(word)
            elif 'CJWH' in word:
                cunzhuang.append(word)
            elif 'ZRCZ' in word:
                cunzhuang.append(word)
            elif 'JLX' in word:
                zhuzhai.append(word)
                cunzhuang.append(word)
                jianzhu.append(word)
            elif 'MPH' in word:
                zhuzhai.append(word)
                cunzhuang.append(word)
                jianzhu.append(word)
            elif 'XIAOQU' in word:
                zhuzhai.append(word)
                jianzhu.append(word)
            elif 'JZW' in word:
                jianzhu.append(word)
            elif 'ZUTUAN' in word:
                zhuzhai.append(word)
            elif 'DYH' in word:
                zhuzhai.append(word)
                cunzhuang.append(word)
                jianzhu.append(word)
            elif 'LOUC' in word:
                zhuzhai.append(word)
                cunzhuang.append(word)
                jianzhu.append(word)
            elif 'HSH' in word:
                zhuzhai.append(word)
                cunzhuang.append(word)
                jianzhu.append(word)
            else:
                pass
        zhuzhai_str = " ".join(zhuzhai)
        cunzhuang_str = " ".join(cunzhuang)
        jianzhu_str = " ".join(jianzhu)
        print(zhuzhai_str)
        print(cunzhuang_str)
        print(jianzhu_str)
        result = []
        result_and = []
        result.extend(self.__search__(zhuzhai))
        result.extend(self.__search__(cunzhuang))
        result.extend(self.__search__(jianzhu))
        if len(result) == 0:
            return ""
        return ",".join(list(set(result)))

    def __search__(self,words):

        t0 = time.time()
        nodes = []
        addrs = []
        addrstxt = []
        print(words,nodes)
        nodes = self.addr_tree.scan_nodes([self.addr_tree.root],words,nodes)
        print(nodes)
        addrstxt = ""
        result=[]
        for node in nodes:
            __result__ = []
            self.addr_tree.scan_child_word(node,__result__)
            result.extend(__result__)
        t1 = time.time()
        result = list(set(result))
        addrstxt = self.addr_tree.get_all_parent_tree(result)
        addrstxt = list(set(addrstxt))
        print('\n> 耗时',t1-t0)
        print('\n> 比对输入',words)
        print('\n> 比对输出',addrstxt)
        return addrstxt

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

    def read_file(self,input_file,delimeter='/'):
        lines = open(input_file,"r").readlines()
        for line in lines:
            line.strip()
            yield line
            #words = line.split(delimeter)
            #yield words

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

    def get_all_parent_tree(self,nodes):
        parstrs = []
        for node in nodes:
            parstr = []
            self.parent_tree(node,parstr)
            parstr = ''.join(parstr[::-1])
            parstrs.append(parstr)
        return parstrs

    def word_match(self,sentence,lth=7):
        '''
        func: filter word in standard lib
        sentence: sentence
        '''
        res = []
        res = self.word_tree.word_match(sentence, res, lth=7)
        print('\n> 标准地址词过滤', res)
        return ' '.join(res)

def random_filter(item):
    #随机丢弃某几个词条，来进行检索
    ll = len(item)
    _item_ = []
    for i in range(ll):
        guess = random.randint(10)
        if guess%2==0:
            continue
        else:
            _item_.append(item[i])

if __name__ == '__main__':
    #init_data.gen_std_tree()
    acti_match_ins = ActiMatch('dummy')
    acti_match_ins.search("内蒙古/PROV 包头市/CITY ")
    pdb.set_trace()
    '''
    sent = '贵州省/贵阳市/云岩区/荷塘社区服务中心/鑫园居委会/白云大道/201号/4栋/3单元/2层/202'
    sent1 = '贵州省/云岩区/荷塘社区服务中心/鑫园居委会/白云大道/201号/4栋/3单元/2层/202'
    sent2 = '贵州省/云岩区/白云大道/201号/4栋/3单元/2层/202'
    sent3 = '白云大道/201号/4栋/3单元/2层/202'
    sent4 = '贵州省/贵阳市/云岩区/顺海安居住宅小区/7栋/2单元/103'
    sent5 = '贵州省/贵阳市/云岩区/顺海安居住宅小区/7栋/2单元/203'
    sent6 = '贵州省/贵阳市/云岩区/顺海安居住宅小区/7栋/2单元/303'
    sent7 = '贵州省/贵阳市/云岩区/顺海安居住宅小区/7栋/2单元/403'
    sent8 = '贵州省/贵阳市/云岩区/顺海安居住宅小区/7栋/2单元/503'
    res = []
    print(acti_match_ins.search(sent.split('/')))
    print(acti_match_ins.search(sent1.split('/')))
    print(acti_match_ins.search(sent2.split('/')))
    print(acti_match_ins.search(sent3.split('/')))
    print(acti_match_ins.search(sent4.split('/')))
    print(acti_match_ins.search(sent5.split('/')))
    print(acti_match_ins.search(sent6.split('/')))
    print(acti_match_ins.search(sent7.split('/')))
    print(acti_match_ins.search(sent8.split('/')))
    '''
    f = open('比对程序测试.txt','a+')
    gen = acti_match_ins.read_file(myconfig.STDTXTPATH)
    acti_match_ins.addr_tree.insert('123')
    acti_match_ins.addr_tree.insert('234')
    acti_match_ins.addr_tree.insert('345')
    acti_match_ins.addr_tree.insert('贵州省')
    acti_match_ins.addr_tree.insert('贵阳市')
    acti_match_ins.addr_tree.insert('贵州省')
    acti_match_ins.addr_tree.insert('云岩区')
    items = gen.__next__()
    #res = acti_match_ins.search(['内蒙古自治区','青山区','11号'])
    print(item)
    from business_ultra.reghelper import RegHelper
    regHelperInstance = RegHelper('dummy')
    while(1):
        item = gen.__next__()
        #line = '内蒙古包头市青山区'
        line = item
        from business_ultra import my_helper
        result = my_helper.address_formula(line)
        print('\r> result', result)
        res = acti_match_ins.search(result)
        #res = acti_match_ins.search([item[0],item[-1]])
        print('\n=====\n>结果: %s\n输入: %s'%(res,item))
        pdb.set_trace()

