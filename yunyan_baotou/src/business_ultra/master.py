#!
'''
this is master file to handle all business jobs
import func add from file task.py
'''

import re
import time
import numpy as np
import pdb
import sys
import os
import myconfig
sys.path.append(os.environ['YUNYAN'])
sys.path.append(os.environ['WORKBENCH'])
from src import myjieba as jieba
import myconfig
import function_ultra
from function_ultra import redis_helper
from function_ultra import utils

sys.path.append('.')
import tasks
r = redis_helper.RedisHelper()

import business_ultra
import src.business_ultra
sys.path.append('.')
sys.path.append('..')

from tasks import hello
from tasks import add

import function_ultra
import business_ultra
from function_ultra.redis_helper import RedisHelper

r = RedisHelper()
'''
rsync call
'''

def gen():
    for line in open(myconfig.STDTXTPATH,'r').readlines():
        yield line

def _gen():
    for line in ['贵州省贵阳市','云岩区中天小区','黔灵山','中坝','北京西路538号','黄山冲20号']:
        yield line

def split(sent):
    print('\n>split 测试拆分 sent: ',sent)
    idx = np.random.randint(10000)
    idxs = str(idx)
    r.set(idxs,sent)
    print('\n>split 保存内容进入redis',sent,idxs)
    result = tasks.split.delay(idxs)
    while not result.ready():
        print('\n> waitting...')
        pass
    '''
    this is may be a risk issue require, haining 090112
    '''
    result_split = r.get(myconfig.SPLIT_RES).decode('utf-8')
    print('\n> 获得SPLIT_RES结果: ', result_split)
    return result_split

def posseg_cut(sent):
    print('\n>split 测试拆分2 sent: ',sent)
    idx = np.random.randint(10000)
    idxs = str(idx)
    r.set(idxs,sent)
    print('\n>split 保存内容进入redis2',sent,idxs)
    result = tasks.posseg_cut.delay(idxs)
    while not result.ready():
        print('\n> waitting...')
        pass
    '''
    this is may be a risk issue require, haining 090112
    '''
    print(r.get('1'))
    print(r.get('2'))
    print(r.get('3'))
    print(r.get('4'))
    print(r.get('5'))
    print(r.get('6'))
    result_split = r.get(myconfig.POSSEG_CUT_RES).decode('utf-8')
    print('\n> 获得POSSEG_CUT_RES结果: ', result_split)
    return result_split

'''
def pred(sent):
    idx = np.random.randint(10000)
    idxs = str(idx)

    r.set(idxs,sent)
    result = tasks.pred.delay(idxs)
    while not result.ready():

        pass
    # this is may be a risk issue require, haining 090112
    pass

    get result
    result_match = r.get(myconfig.PRED_RES).decode('utf-8')
    return result_match
'''

def search(sent):
    idx = np.random.randint(10000)
    idxs = str(idx)
    r.set(idxs,sent)
    result = tasks.search.delay(idxs)
    while not result.ready():
        pass
    '''
    this is may be a risk issue require, haining 090112
    '''
    pass

    '''
    get result
    '''
    result_match = r.get(myconfig.SEARCH_RES).decode('utf-8')
    return result_match

def word_match(sent):
    idx = np.random.randint(10000)
    idxs = str(idx)
    r.set(idxs,sent)
    result = tasks.word_match.delay(idxs)
    while not result.ready():

        pass
    '''
    this is may be a risk issue require, haining 090112
    '''

    pass

    '''
    get result
    '''
    result_match = r.get(myconfig.MATCH_RES).decode('utf-8')
    return result_match

def test():
    gl = open('0113_shequjingwu_match_split.txt','a+')
    g = gen()
    while(1):
        print('=========================time %s============================'%str(time.time()))
        sent = g.__next__()
        if not '云岩区' in sent:
            continue
        sents = sent.split(',')
        print('sent',sent)
        for _sent in sents:
          if len(_sent)<2:
              continue
          sent = _sent
          dl = re.findall('\d+',sent)
          wd = re.findall('\D+',sent)
          sent_base = ''
          if len(wd)>0:
              sent_base+=wd[0][-3:]
          sent_base+=("".join(dl))

          gl.write('过滤 %s\n'%sent)
          result_txt = match(sent)

          gl.write('%s\n'%result_txt[0])
          print('result_match',result_txt[0])
          gl.write('%s\n'%result_txt[1])
          print('result_split',result_txt[1])
          gl.write('========拆标准地址=========time %s ==========找样本地址==========\n'%str(time.time()))

          gl.write('拆分 %s\n'%sent)
          result_txt = split(sent)

          gl.write('%s\n'%result_txt[0])
          print('result_match',result_txt[0])
          gl.write('%s\n'%result_txt[1])
          print('result_split',result_txt[1])
          gl.write('========拆标准地址=========time %s ==========找样本地址==========\n'%str(time.time()))

          gl.write('查找 %s\n'%sent_base)
          result_txt = split(wd)

          gl.write('%s\n'%result_txt[0])
          print('result_match',result_txt[0])
          gl.write('%s\n'%result_txt[1])
          print('result_split',result_txt[1])
          gl.write('========拆标准地址=========time %s ==========找样本地址==========\n'%str(time.time()))

if __name__ == '__main__':
    test()

