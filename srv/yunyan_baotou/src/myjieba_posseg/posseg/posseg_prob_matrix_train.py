import numpy as np
import sys
import re
from collections import OrderedDict
import pdb
"""
读取分词后的文本，对分词结果进行统计
"""

my_inf = '-3.14e+100'

labels_ad1_order = OrderedDict()
labels_ad1_order['省'] = 'PROV'
labels_ad1_order['市'] = 'CITY'
labels_ad1_order['区'] = 'DIST'
labels_ad1_order['社区'] = 'SHEQU'
labels_ad1_order['村居委会'] = 'CJWH'
labels_ad1_order['自然村组'] = 'ZRCZ'
labels_ad1_order['街路巷名'] = 'JLX'
labels_ad1_order['门牌号'] = 'MPH'
labels_ad1_order['小区名'] = 'XIAOQU'
labels_ad1_order['组团名称'] = 'ZUTUAN'
labels_ad1_order['建筑物名称'] = 'JZW'
labels_ad1_order['栋号'] = 'DONGHAO'
labels_ad1_order['单元号'] = 'DYH'
labels_ad1_order['楼层'] = 'LOUC'
labels_ad1_order['户室号'] = 'HSH'
labels_ad1_order['其他数字'] = 'm'
labels_ad1_order['其他字符'] = 'x'
labels_ad1_order['其他英文字符'] = 'eng'

labels_ad2_order = OrderedDict()
for k in labels_ad1_order.keys():
    labels_ad2_order[labels_ad1_order[k]] = k
print(labels_ad2_order)
pdb.set_trace()
f11 = open('train_prob_matrix1.txt', 'r', encoding='utf-8')
lines = []
for line in f11.readlines():
    if line[-3] == 'r':
        continue
        pass
    lines.append(line)
f11.close()

def cnt_prob_start(lines):
    keys1 = ['B','M','E','S']
    keys2 = list(labels_ad2_order.keys())
    keys3 = []
    for k1 in keys1:
        for k2 in keys2:
            keys3.append((k1,k2))
    kv = {}
    for kk in keys3:
        kv[kk] = 0
    for line in lines:
        line = re.sub("\n","",line)
        while line:
            index1 = line.find('/')
            index2 = line.find(' ')
            word = line[0:index1]
            pos = line[index1+1:index2]
            lenth = len(word)
            if lenth == 1:
                kv[('S', pos)] += 1
            elif lenth == 2:
                kv[('B', pos)] += 1
                kv[('E', pos)] += 1
            elif lenth > 2:
                kv[('B', pos)] += 1
                kv[('E', pos)] += 1
                kv[('M', pos)] += lenth - 2
            line = line[index2+1:]
    return kv


prob_start = cnt_prob_start(lines)
isum = sum(list(prob_start.values()))
f = open("prob_start.py","w+")
f.write("P={\n")
for key in prob_start.keys():
    f.write(str(key)+': ')
    if prob_start[key] == 0:
        f.write(my_inf)
    else:
        f.write(str(np.log(prob_start[key]/isum)))
    f.write(',\n')
f.write("}\n")
f.close()


def cnt_prob_emit(lines):
    chars_keys = {}
    keys1 = ['B','M','E','S']
    keys2 = list(labels_ad2_order.keys())
    keys3 = []
    for k1 in keys1:
        for k2 in keys2:
            keys3.append((k1, k2))

    for kk in keys3:
        chars_keys[kk] = {}

    for line in lines:
        line = re.sub("\n","",line)
        while line:
            index1 = line.find('/')
            index2 = line.find(' ')
            word = line[0:index1]
            pos = line[index1+1:index2]
            lenth = len(word)
            line = line[index2+1:]
            if lenth == 1:
                if word[0] not in chars_keys[('S', pos)].keys():
                    chars_keys[('S', pos)][word[0]] = 1
                else:
                    chars_keys[('S', pos)][word[0]] += 1
            elif lenth == 2:
                if word[0] not in chars_keys[('B', pos)].keys():
                    chars_keys[('B', pos)][word[0]] = 1
                else:
                    chars_keys[('B', pos)][word[0]] += 1
                if word[1] not in chars_keys[('E', pos)].keys():
                    chars_keys[('E', pos)][word[1]] = 1
                else:
                    chars_keys[('E', pos)][word[1]] += 1
            elif lenth > 2:
                if word[0] not in chars_keys[('B', pos)].keys():
                    chars_keys[('B', pos)][word[0]] = 1
                else:
                    chars_keys[('B', pos)][word[0]] += 1
                if word[-1] not in chars_keys[('E', pos)].keys():
                    chars_keys[('E', pos)][word[-1]] = 1
                else:
                    chars_keys[('E', pos)][word[-1]] += 1
                for i in range(1, lenth-1):
                    if word[i] not in chars_keys[('M', pos)].keys():
                        chars_keys[('M', pos)][word[i]] = 1
                    else:
                        chars_keys[('M', pos)][word[i]] += 1

    return chars_keys


prob_emit = cnt_prob_emit(lines)
f = open("prob_emit.py", "w+")
f.write("from __future__ import unicode_literals\n")
f.write("P = {\n")
for key in prob_emit:
    f.write(str(key))
    f.write(': {')
    sum1 = 0
    for key1 in prob_emit[key].keys():
        sum1 += prob_emit[key][key1]
    for key1 in prob_emit[key].keys():
        prob_emit[key][key1] /= sum1

    for char in prob_emit[key].keys():
        if not len(hex(ord(char))) == 6:
            continue

        f.write("'\\u%s': %s,\n" % (hex(ord(char))[2:], np.log(prob_emit[key][char]/sum1)))
        # f.write(str(np.log(prob_emit[key][char]/sum1)))

    f.write("},\n")
f.write("}\n")
f.close()


def cnt_prob_trans(lines):
    keys1 = ['B','M','E','S']
    keys2 = list(labels_ad2_order.keys())
    keys3 = []
    for k1 in keys1:
        for k2 in keys2:
            keys3.append((k1, k2))

    # keys = {"BE","BM","EB","ES","ME","MM","SB","SS"}
    kvs = {}
    for kk in keys3:
        kvs[kk] = {}
    for line in lines:
        line = re.sub("\n","",line)
        word_list = []
        pos_list = []
        while line:
            index1 = line.find('/')
            index2 = line.find(' ')
            word = line[0:index1]
            pos = line[index1+1:index2]
            word_list.append(word)
            pos_list.append(pos)
            line = line[index2+1:]
        for ii in range(len(word_list)-1):
            lenth = len(word_list[ii])
            sym = ''
            if len(word_list[ii+1]) > 1:
                sym += 'B'
            else:
                sym += 'S'

            if lenth == 1:
                if (sym, pos_list[ii+1]) not in kvs[('S',  pos_list[ii])].keys():
                    kvs[('S',  pos_list[ii])][sym, pos_list[ii+1]] = 1
                else:
                    kvs[('S', pos_list[ii])][sym, pos_list[ii + 1]] += 1
            if lenth == 2:
                if ('E', pos_list[ii]) not in kvs[('B',  pos_list[ii])].keys():
                    kvs[('B',  pos_list[ii])]['E', pos_list[ii]] = 1
                else:
                    kvs[('B', pos_list[ii])]['E', pos_list[ii]] += 1
                if (sym, pos_list[ii+1]) not in kvs[('E',  pos_list[ii])].keys():
                    kvs[('E',  pos_list[ii])][sym, pos_list[ii+1]] = 1
                else:
                    kvs[('E', pos_list[ii])][sym, pos_list[ii + 1]] += 1
            elif lenth >= 3:
                if ('M', pos_list[ii]) not in kvs[('B',  pos_list[ii])].keys():
                    kvs[('B',  pos_list[ii])]['M', pos_list[ii]] = 1
                else:
                    kvs[('B', pos_list[ii])]['M', pos_list[ii]] += 1
                if ('E', pos_list[ii]) not in kvs[('M',  pos_list[ii])].keys():
                    kvs[('M',  pos_list[ii])]['E', pos_list[ii]] = 1
                else:
                    kvs[('M', pos_list[ii])]['E', pos_list[ii]] += 1
                if ('M', pos_list[ii]) not in kvs[('M',  pos_list[ii])].keys():
                    if lenth > 3:
                        kvs[('M',  pos_list[ii])]['M', pos_list[ii]] = lenth-3
                else:
                    kvs[('M', pos_list[ii])]['M', pos_list[ii]] += lenth-3
                if (sym, pos_list[ii+1]) not in kvs[('E',  pos_list[ii])].keys():
                    kvs[('E',  pos_list[ii])][sym, pos_list[ii+1]] = 1
                else:
                    kvs[('E', pos_list[ii])][sym, pos_list[ii + 1]] += 1

    return kvs


prob_trans = cnt_prob_trans(lines)

f = open("prob_trans.py","w+")
f.write("P={\n")
for key in prob_trans.keys():
    sum1 = 0
    f.write(str(key))
    f.write(': {')

    for key1 in prob_trans[key].keys():
        sum1 += prob_trans[key][key1]
    if sum == 0:
        f.write('},\n')
    else:
        for key1 in prob_trans[key].keys():
            f.write(str(key1))
            f.write(':')
            prob_trans[key][key1] = np.log(prob_trans[key][key1]/(1+sum1))
            f.write(str(prob_trans[key][key1]))
            f.write(',\n')
        f.write('},\n')
f.write("}\n")
f.close()
del lines
