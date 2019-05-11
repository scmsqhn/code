import numpy as np
import sys
import re
import collections
"""
读取分词后的文本，对分词结果进行统计
"""
trans_dict = {}
stats_dict = {}

def log_keys(kvs):
    sum_result = 0.0
    for k in kvs:
        print(k)
        print(kvs[k])
        sum_result+=float(kvs[k])
    kvs_out = kvs.copy()
    for k in kvs:
        kvs_out[k] == np.log(float(kvs[k])/sum_result)
    return kvs_out
        

def read_file(filepath):
    with open(filepath,"r") as f:
        lines = f.readlines()
        return lines

filepath = sys.argv[1]
lines = read_file(filepath)

def cnt_prob_start(lines):
    keys = ['B','M','E','S']
    kv = {}
    for k in keys:
        kv[k] = 0
    for line in lines:
        line = re.sub("\n","",line)
        lenth = len(line)
        if lenth == 1:
            kv['S']+=1
        elif lenth == 2:
            kv['B']+=1
            kv['E']+=1
        elif lenth > 2:
            kv['B']+=1
            kv['E']+=1
            kv['M']+=lenth-2
    return kv

prob_start = cnt_prob_start(lines)

def cnt_prob_emit(lines):
    chars_keys = {}
    keys = ['B','M','E','S']
    lst_B,lst_M,lst_E,lst_S = [],[],[],[]
    for line in lines:
        line = re.sub("\n","",line)
        lenth = len(line)
        if lenth == 1:
             lst_S.extend([line])
        elif lenth == 2:
             lst_B.extend([line[0]])
             lst_E.extend([line[-1]])
        elif lenth > 2:
             lst_B.extend([line[0]])
             lst_E.extend([line[-1]])
             for char in line[1:-1]:
                 lst_M.extend([char])
    chars_keys['B'] = dict(collections.Counter(lst_B))
    chars_keys['E'] = dict(collections.Counter(lst_E))
    chars_keys['M'] = dict(collections.Counter(lst_M))
    chars_keys['S'] = dict(collections.Counter(lst_S))
    return chars_keys

prob_emit = cnt_prob_emit(lines)

def cnt_prob_trans(lines):
    keys = {"BE","BM","EB","ES","ME","MM","SB","SS"}
    kvs = {}
    for k in keys:
        kvs[k] = 0
    for line in lines:
        line = re.sub("\n","",line)
        lenth = len(line)
        if lenth == 2:
            kvs['BE'] += 1
        elif lenth == 3:
            kvs['BM'] += 1
            kvs['ME'] += 1
        elif lenth > 3:
            kvs['BM'] += 1
            kvs['ME'] += 1
            kvs['MM'] += lenth-3
    return kvs

prob_trans = cnt_prob_trans(lines)

del lines
