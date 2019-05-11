import numpy as np
import os
import sys
import re
import pickle
from collections import OrderedDict
import pdb
import sample_generate
basedir1 = os.path.dirname(os.path.abspath(__file__))
"""
读取分词后的文本，对分词结果进行统计
"""

my_inf = -3.14e+100

labels_ad1_order = OrderedDict()
labels_ad1_order['街路巷名'] = 'JLX'
labels_ad1_order['门牌号'] = 'MPH'
labels_ad1_order['村居委会'] = 'cunjuweihui'
labels_ad1_order['社区'] = 'shequ'
labels_ad1_order['LOC'] = 'nz'
labels_ad1_order['eng'] = 'eng'
labels_ad1_order['ns'] = 'ns'
labels_ad1_order['nr'] = 'nr'
labels_ad1_order['市'] = 'shi'
labels_ad1_order['区'] = 'qu'
labels_ad1_order['自然村组'] = 'zirancunzu'
labels_ad1_order['小区名'] = 'xiaoquming'
labels_ad1_order['楼层'] = 'louceng'
labels_ad1_order['栋号'] = 'donghao'
labels_ad1_order['单元号'] = 'danyuanhao'
labels_ad1_order['建筑物名称'] = 'jianzhuwumingcheng'
labels_ad1_order['组团名称'] = 'zutuanmingcheng'

possegs = [line.strip() for line in open('posseg.txt','r').readlines()]
possegs.append('in')
possegs.append('jn')
possegs.append('bg')
print(possegs)
for i in possegs:
    #labels_ad1_order['OTHER'] = i
    labels_ad1_order[i] = i

labels_ad2_order = OrderedDict()

for k in labels_ad1_order.keys():
    labels_ad2_order[labels_ad1_order[k]] = k

dist_beijing = ['东城区', '西城区', '朝阳区', '丰台区', '石景山区', '海淀区', '房山区', '怀柔区',
                '通州区', '顺义区', '昌平区', '大兴区', '门头沟区', '平谷区', '密云区', '延庆区']
words_del = ['东里', '西里', '南里', '北里', '中里', '东大街', '西大街', '东路', '西路', '南路',
             '北路', '中路','南大街', '北大街', '胡同', '内大街', '外大街', '一里', '二里', '三里',
             '四里', '东街', '西街', '南街', '北街', '中街', '国际大厦', '北京', '北京市', '中国']
words_jlx = ['北下关', '西小口路', '海友酒店', '和光里', '阳光好东东', '桑峪村', '西北旺', '真武庙3条',
             '崔村镇', '嘉园商业街', '太平庄中街', '单村北口站', '东北旺西路','中关村软件园',
             '大耕垡路', '张大路', '鼓楼街道', '阳光街', '莲花河东侧路', '荣华中路',
             '北京植物园', '纪家庙路', '首经贸中街', '北蜂窝中路', '北蜂窝西路', '康辛路']
words_zutuan = ['东三区', '东南门']
words_mph = ['首层']


def cnt_prob_start(lines):
    keys1 = ['B', 'M', 'E', 'S']
    keys2 = list(labels_ad2_order.keys())
    keys3 = []
    for k1 in keys1:
        for k2 in keys2:
            keys3.append((k1,k2))
    kv = {}
    for kk in keys3:
        kv[kk] = 0
    for line in lines:
        for wp in line:
            word = wp[0]
            pos = wp[1]
            lenth = len(word)
            if lenth == 1 and ('S', pos) in kv.keys():
                kv[('S', pos)] += 1
            elif lenth >= 2 and ('B', pos) in kv.keys():
                kv[('B', pos)] += 1

    return kv


def cnt_prob_emit(lines):
    chars_keys = {}
    keys1 = ['B', 'M', 'E', 'S']
    keys2 = list(labels_ad2_order.keys())
    keys3 = []
    for k1 in keys1:
        for k2 in keys2:
            keys3.append((k1, k2))

    for kk in keys3:
        chars_keys[kk] = {}

    for line in lines:
        for wp in line:
            word = wp[0]
            pos = wp[1]
            lenth = len(word)
            if pos not in labels_ad2_order.keys():
                continue
                pass

            if lenth == 1:
                if word[0] not in chars_keys[('S', pos)].keys():
                    chars_keys[('S', pos)][word[0]] = 1
                else:
                    chars_keys[('S', pos)][word[0]] += 1

            if lenth >= 2:
                if word[0] not in chars_keys[('B', pos)].keys():
                    chars_keys[('B', pos)][word[0]] = 1
                else:
                    chars_keys[('B', pos)][word[0]] += 1
                if word[-1] not in chars_keys[('E', pos)].keys():
                    chars_keys[('E', pos)][word[-1]] = 1
                else:
                    chars_keys[('E', pos)][word[-1]] += 1

            if lenth > 2:
                for i in range(1, lenth - 1):
                    if word[i] not in chars_keys[('M', pos)].keys():
                        chars_keys[('M', pos)][word[i]] = 1
                    else:
                        chars_keys[('M', pos)][word[i]] += 1

    return chars_keys


def cnt_prob_trans(lines):
    keys1 = ['B', 'M', 'E', 'S']
    keys2 = list(labels_ad2_order.keys())
    keys3 = []
    for k1 in keys1:
        for k2 in keys2:
            keys3.append((k1, k2))

    kvs = {}
    for kk in keys3:
        kvs[kk] = {}
    for line in lines:
     try:
        word_list = []
        pos_list = []
        for wp in line:
            word = wp[0]
            pos = wp[1]
            word_list.append(word)
            pos_list.append(pos)

        for ii in range(len(word_list) - 1):
            lenth = len(word_list[ii])
            sym = ''
            if len(word_list[ii+1]) == 1:
                sym += 'S'
            else:
                sym += 'B'

            if lenth == 1:
                if (sym, pos_list[ii + 1]) not in kvs[('S', pos_list[ii])].keys():
                    kvs[('S', pos_list[ii])][sym, pos_list[ii + 1]] = 1
                else:
                    kvs[('S', pos_list[ii])][sym, pos_list[ii + 1]] += 1

            if lenth > 1:
                if (sym, pos_list[ii + 1]) not in kvs[('E', pos_list[ii])].keys():
                    kvs[('E', pos_list[ii])][sym, pos_list[ii + 1]] = 1
                else:
                    kvs[('E', pos_list[ii])][sym, pos_list[ii + 1]] += 1

            if lenth == 2:
                if ('E', pos_list[ii]) not in kvs[('B', pos_list[ii])].keys():
                    kvs[('B', pos_list[ii])]['E', pos_list[ii]] = 1
                else:
                    kvs[('B', pos_list[ii])]['E', pos_list[ii]] += 1

            if lenth >= 3:
                if ('M', pos_list[ii]) not in kvs[('B', pos_list[ii])].keys():
                    kvs[('B', pos_list[ii])]['M', pos_list[ii]] = 1
                else:
                    kvs[('B', pos_list[ii])]['M', pos_list[ii]] += 1
                if ('E', pos_list[ii]) not in kvs[('M', pos_list[ii])].keys():
                    kvs[('M', pos_list[ii])]['E', pos_list[ii]] = 1
                else:
                    kvs[('M', pos_list[ii])]['E', pos_list[ii]] += 1

            if lenth > 3:
                if ('M', pos_list[ii]) not in kvs[('M', pos_list[ii])].keys():
                    kvs[('M', pos_list[ii])]['M', pos_list[ii]] = lenth - 3
                else:
                    kvs[('M', pos_list[ii])]['M', pos_list[ii]] += lenth - 3

        lenth = len(word_list[-1])

        if lenth == 2:
            if ('E', pos_list[-1]) not in kvs[('B', pos_list[-1])].keys():
                kvs[('B', pos_list[-1])]['E', pos_list[-1]] = 1
            else:
                kvs[('B', pos_list[-1])]['E', pos_list[-1]] += 1

        if lenth >= 3:
            if ('M', pos_list[-1]) not in kvs[('B', pos_list[-1])].keys():
                kvs[('B', pos_list[-1])]['M', pos_list[-1]] = 1
            else:
                kvs[('B', pos_list[-1])]['M', pos_list[-1]] += 1
            if ('E', pos_list[-1]) not in kvs[('M', pos_list[-1])].keys():
                kvs[('M', pos_list[-1])]['E', pos_list[-1]] = 1
            else:
                kvs[('M', pos_list[-1])]['E', pos_list[-1]] += 1

        if lenth > 3:
            if ('M', pos_list[-1]) not in kvs[('M', pos_list[-1])].keys():
                kvs[('M', pos_list[-1])]['M', pos_list[-1]] = lenth - 3
            else:
                kvs[('M', pos_list[-1])]['M', pos_list[-1]] += lenth - 3
     except KeyError:
           print(line)
           continue
     except IndexError:
           print(line)
           continue
    return kvs


def hmm_matrix_train(lines_t):
    prob_start = cnt_prob_start(lines_t)
    isum = sum(list(prob_start.values()))
    for key in prob_start.keys():
        if prob_start[key] == 0:
            prob_start[key] = my_inf
        else:
            prob_start[key] = np.log(prob_start[key] / isum)

    prob_emit = cnt_prob_emit(lines_t)
    for key in prob_emit:
        sum1 = 0
        for key1 in prob_emit[key].keys():
            sum1 += prob_emit[key][key1]
        for char in prob_emit[key].keys():
            prob_emit[key][char] = np.log(prob_emit[key][char] / sum1)

    prob_trans = cnt_prob_trans(lines_t)
    for key in prob_trans.keys():
        sum1 = 0
        for key1 in prob_trans[key].keys():
            sum1 += prob_trans[key][key1]
        for key1 in prob_trans[key].keys():
            prob_trans[key][key1] = np.log(prob_trans[key][key1] / (1 + sum1))

    fm = open(basedir1+'/hmm_matrix.pkl', 'wb')
    pickle.dump([prob_start, prob_trans, prob_emit], fm)
    fm.close()

    return prob_start, prob_trans, prob_emit


def dict_train(min_num1, min_num2, min_num3, lines_t):
    dict_res = OrderedDict()
    dict_res['街路巷名'] = OrderedDict()
    dict_res['门牌号'] = OrderedDict()

    for line in lines_t:
        for wp in line:
            word = wp[0]
            pos = wp[1]
            if len(word) > 1 and pos in dict_res.keys():
                if word not in dict_res[pos].keys():
                    dict_res[pos][word] = 101
                else:
                    dict_res[pos][word] += 1

    dict_p = dict_res

    my_dict = OrderedDict()

    for w in dict_p['街路巷名'].keys():
        if w in words_del:
            continue
            pass
        if len(w) <= 2:
            if dict_p['街路巷名'][w] < min_num1:
                continue
                pass
        elif len(w) == 3:
            if dict_p['街路巷名'][w] < min_num2:
                continue
                pass
        else:
            if dict_p['街路巷名'][w] < min_num3:
                continue
                pass
        if w not in my_dict.keys():
            my_dict[w] = (str(dict_p['街路巷名'][w]), '街路巷名')
        else:
            if int(my_dict[w][0]) < dict_p['街路巷名'][w]:
                my_dict[w] = (str(dict_p['街路巷名'][w]), '街路巷名')

    for word in words_jlx:
        my_dict[word] = ('99', '街路巷名')

    for word in dist_beijing:
        my_dict[word] = ('99', '街路巷名')

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
               'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    nums_chinese = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
    for num in nums_chinese:
        my_dict['地铁' + num + '号线'] = ('99', '街路巷名')

    f1 = open(basedir1+'/../dict.txt', 'w', encoding='utf-8')
    for wp in my_dict.keys():
        f1.write(wp)
        f1.write(' ')
        f1.write(my_dict[wp][0])
        f1.write(' ')
        f1.write(my_dict[wp][1])
        f1.write('\n')
    f1.close()


if __name__ == '__main__':

    lines_tr = []
    fq = open(basedir1+'/hmm_train_data.txt', 'r', encoding='utf-8')

    for line in fq.readlines():
        print(line)
        line = re.sub("\n", "", line)
        wp = []
        __line__ = ''
        while line:

            index1 = line.find('/')
            index2 = line.find(' ')
            word = line[0:index1]
            pos = line[index1+1:index2]
            pos = sample_generate.kv(pos)
            line = line[index2+1:]
            print(word,pos)
            wp.append((word, pos))
            if line == __line__:
                break
            __line__ = line
        if wp not in lines_tr:
            lines_tr.append(wp)
            print(wp)
    fq.close()

    print('there are '+str(len(lines_tr))+' addresses for training')
    hmm_matrix_train(lines_tr)
    dict_train(104, 102, 101, lines_tr)

    a = 1

