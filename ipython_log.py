# IPython log file


import pickle
get_ipython().run_line_magic('pinfo', 'pickle.dump')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('pwd', '-P')
get_ipython().run_line_magic('cd', '~')
get_ipython().run_line_magic('cd', 'code')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', 'yunyan_baotou/')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', 'src/')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', 'function_ultra/')
get_ipython().run_line_magic('ls', '')
pickle.load('pk.pkl')
a = pickle.load(open('pk.pkl','rb'))
a
b = pickle.load(open('pk.pkl','rb'))
b
c = pickle.load(open('pk.pkl','rb'))
c
(a,b,c) = pickle.loads(open('pk.pkl','rb'))
(a,b,c) = pickle.loads(open('pk.pkl','rb'))
(a,b,c) = pickle.load(open('pk.pkl','rb'))
a
b
c
c
np.array(c)
c
c
c.fillna(0.0)
d = np.array(c)
d
d.shape
c.shape
list(c.shape)
c
c=0.0
c
(a,b,c) = pickle.load(open('pk.pkl','rb'))
c
c.values
c.values = np.array(c.shape)
get_ipython().run_line_magic('pinfo', 'c.apply')
import word_discover
get_ipython().run_line_magic('ls', '')
from word_discover import *
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('load', 'word_discover.py')
# %load word_discover.py
import networkx as nx
import re
import pdb
import matplotlib.pyplot as plt
import networkx as nx
import os
import sys
import traceback
import matplotlib.pyplot as plt
import re
import pickle
from collections import Counter
import numpy as np
import pandas as pd

sort_edges = lambda dig: sorted(list(dig.edges.items()), key=lambda x:x[-1]['weight'], reverse=True)


gen_lines = lambda lines: [str(line.strip()) for line in lines]



def clr(ustring):
    rstring = strQ2B(ustring)
    rstring = re.sub("[^\u4e00-\u9fa50-9a-zA-Z-]","",rstring)
    rstring = re.sub("'","",rstring)
    rstring = re.sub("-","",rstring)
    return rstring



def strQ2B(ustring):
      rstring = ""
      for uchar in ustring:
          inside_code = ord(uchar)
          if inside_code == 12288:  # 全角空格直接转换
              inside_code = 32
          elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
              inside_code -= 65248
          rstring += chr(inside_code)
      return rstring



def open_file(fn):
    lines = []
    with open(fn, 'r') as f:
        lines = f.readlines()
        np.random.shuffle(lines)
        lines = [clr(line) for line in lines[:1000]]
    return lines


def vocab(fn):
    dct = {}
    lines = open_file(fn)
    for line in lines:
        for char in line:
            if dct.get(char, -1) == -1:
                dct[char]=str(len(dct))
    return dct


def dig_2_table(dig):
    table_dct = {}
    for nodeA in dig.nodes:
        for nodeB in dig.nodes:
            if nodeA == nodeB:
                continue
            if dig.has_node(nodeA):
                if dig.has_node(nodeB):
                    if dig.has_edge(nodeA, nodeB):
                        flag = table_dct.get(nodeA, {})
                        if flag == {}:
                            table_dct[nodeA] = {}
                            table_dct[nodeA][nodeB] = dig.edges[(nodeA, nodeB)]['weight']
                        elif flag.get(nodeB, -1) == -1:
                            table_dct[nodeA][nodeB] = dig.edges[(nodeA, nodeB)]['weight']
                        else:
                            print('table contained')
    return pd.DataFrame(table_dct)



def init_dig(fn):
    '''
    文本生成图
    '''
    dig = nx.DiGraph()
    lines = open_file(fn)
    generator = gen_lines(lines)
    for line in generator:
        if len(line)<2:
            print('only one char here')
            continue
        for index in range(len(line)- 1):
            if dig.has_node(line[index]):
                if dig.has_node(line[index+ 1]):
                    if dig.has_edge(line[index], line[index+ 1]):
                        dig.edges[line[index], line[index+ 1]]['weight']+=1
                        continue
            dig.add_edges_from([(line[index], line[index+ 1])], weight=1)
    return dig


def filter(score, dig):
    result = {}
    edges = sort_edges(dig)
    for edge in edges:
        print(edge)
        if edge[-1]['weight']<score:
            continue
        try:
            result[''.join(edge[0])] = edge[- 1]
        except:
            traceback.print_exc()
    return result


def combine(score, words):
    result = {}
    for word in words:
        for _word in words:
            if word[- 1] == _word[0]:
                if np.log(1.2 + (np.abs(words[word]['weight'] - words[_word]['weight']))) < score:
                    kw = word[:-1]+ _word
                    result[kw] = words[word]['weight']+ words[_word]['weight']
                else:
                    result[word] = words[word]['weight']
                    result[_word] = words[_word]['weight']
    return result


def calcu(dig, gen,  filter_score, combine_score):
    '''
    measure the cut result, tensorflow loss, purpose is make the words less
    and less, that the language's  efficient
    '''
    result = []
    kv = filter(filter_score, dig)
    print(kv)
    short_kv = combine(combine_score, kv)
    words = [k for k in short_kv]
    result.extend(words)
    try:
        rule = re.compile(str(words))
    except:
        pdb.set_trace()
    # words if the words we discovery
    for line in gen:
        print(line)
        wds = list(re.split(rule, line))
        for wd in wds:
            if not wd == '':
                result.append(wd)
    print(result)
    words_num = len(list(set(result)))
    qifu_score = qifu_count(result)
    print('words_num', words_num, 'qifu_score' , qifu_score)
    with open('result','w+') as outf:
        outf.write("%s\n"%(words_num))
        outf.write("%s\n"%(qifu_score))
        outf.write(str(result)+"\n")
    return words_num, qifu_score


def qifu_count(result):
    total = len(result)
    cnt=1
    loss = 0
    qifu_counter = Counter(result)
    words = sorted(list(qifu_counter.items()), key=lambda x: x[-1], reverse=True)
    for word in words:
        loss += np.log(1.2 + np.abs(qifu_counter[word] - (total / cnt)))
    return loss

def arr_genrerate(filter_score_min, filter_step_num, filter_step, combine_score_min, combine_step_num, combine_step, fn):
    dig = init_dig(fn)
    gen = gen_lines(open_file(fn))
    res_lst = []
    for i in range(filter_step_num):
        filter_level = filter_score_min+filter_step*i
        for j in range(combine_step_num):
            combine_level = combine_score_min+combine_step*j
            words_num, qifu_score = calcu(dig, gen, filter_level, combine_level)
            res = [filter_level, combine_level, words_num, qifu_score]
            res_lst.append(res)
    return np.array(res_lst)


def show_connect_table(df, words):
    df.loc[:,:]=0.0
    for word in words:
        if len(word)<2:
            continue
        for index in range(len(word)-1):
            df.loc[word[index],word[index+1]] = 1
    return df


if __name__ == '__main__':
    #words_num, qifu_score = calcu(fn='/home/siy/data/广电全量地址_weak.csv', filter_score=0.4, combine_score=0.1)
    arr = arr_genrerate(filter_score_min=0.0, filter_step_num=20, filter_step=2, combine_score_min=0.0, combine_step_num=20, combine_step=2, fn='/home/siy/data/广电全量地址_weak.csv')
    pickle.dump(arr, open('pkl.pkl','wb'))
    pdb.set_trace()
get_ipython().run_line_magic('ls', '')
show_connect_table()
pk = pickle.load('pkl.pkl')
pk = pickle.load(open('pkl.pkl','rb'))
pk
pk
pk[0]
pk[1]
pk[3]
pickle.load('pkl.pkl')
pickle.load(open('pkl.pkl','rb'))
df = pickle.load(open('pkl.pkl','rb'))
df
df.shape
df
type(df)
df[0]
df[1]
df[2]
df[3]
df[4]
df[2]
df[1]
en("(df[1])")
len(df[1])
df
dig.degree
dig.degree['市']
pow()
np.pow
pow()
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('run', 'word_discover.py')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', '..')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', '..')
get_ipython().run_line_magic('cd', '..')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', 'word_discover/')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('run', 'discover.py')
import power
power
np.power()
get_ipython().run_line_magic('run', 'discover.py')
get_ipython().run_line_magic('run', 'discover.py')
get_ipython().run_line_magic('run', 'discover.py')
get_ipython().run_line_magic('run', 'discover.py')
get_ipython().run_line_magic('run', 'discover.py')
get_ipython().run_line_magic('run', 'discover.py')
get_ipython().run_line_magic('run', 'discover.py')
