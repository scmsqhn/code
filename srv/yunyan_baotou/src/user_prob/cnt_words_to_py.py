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
isum = sum(list(prob_start.values()))
with open("prob_start.py","w+") as f:
    f.write("P={\n")
    for k in ["B","M","E","S"]:
        f.write("'%s': %s,\n"%(k,np.log(prob_start[k]/isum)))
    f.write("}\n")

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
isum = 0
isum+=sum(list(prob_emit['B'].values()))
isum+=sum(list(prob_emit['M'].values()))
isum+=sum(list(prob_emit['S'].values()))
isum+=sum(list(prob_emit['E'].values()))
with open("./prob_emit.py","w+") as f:
    f.write("from __future__ import unicode_literals\n")
    f.write("P = {\n")
    for k in prob_emit:
        f.write("'%s':{\n"%k)
        for char in prob_emit[k]:
            #print("'\u%s': %s"%(hex(ord(char)),prob_emit[k][char]))
            if not len(hex(ord(char))) == 6:
                continue
            f.write("'\\u%s': %s,\n"%(hex(ord(char))[2:],np.log(prob_emit[k][char]/isum)))
        f.write("},\n")
    f.write("}\n")
            
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
bsum = prob_trans['BE']+prob_trans['BM']+1
esum = prob_trans['EB']+prob_trans['ES']+1
msum = prob_trans['ME']+prob_trans['MM']+1
ssum = prob_trans['SB']+prob_trans['SS']+1
print(bsum,esum,msum,ssum)
with open("prob_trans.py","w+") as f:
    f.write("P={\n")
    f.write(re.sub("-inf","-100","'B': {'E': %s, 'M': %s},\n"%(np.log(prob_trans['BE']/(1+bsum)),np.log(prob_trans['BM']/(1+bsum)))))
    f.write(re.sub("-inf","-100","'E': {'B': %s, 'S': %s},\n"%(np.log(prob_trans['EB']/(1+esum)),np.log(prob_trans['ES']/(1+esum)))))
    f.write(re.sub("-inf","-100","'M': {'E': %s, 'M': %s},\n"%(np.log(prob_trans['ME']/(1+msum)),np.log(prob_trans['MM']/(1+msum)))))
    f.write(re.sub("-inf","-100","'S': {'B': %s, 'S': %s}\n}"%(np.log(prob_trans['SB']/(1+ssum)),np.log(prob_trans['SS']/(1+ssum)))))
del lines
