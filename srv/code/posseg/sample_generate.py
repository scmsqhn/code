# !/encoding=utf-8

# ================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: sample_generate.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-09
#   describe:
# ================================================================
import requests
import json
import jieba
import jieba.posseg
print(jieba.posseg.__path__)
import pdb
import os
import sys
import numpy as np
'''
jieba.load_userdict('./dict/userdict.txt')
jieba.load_userdict('./dict/sheng_shi_qu.txt')
jieba.load_userdict('./dict/sheng_dict.txt')
jieba.load_userdict('./dict/shi_dict.txt')
jieba.load_userdict('./dict/qu_dict.txt')
'''

def init_user_dict():
    pf = os.walk(os.path.join("./dict"))
    #jieba.load_userdict(os.path.join(CURPATH,'../dct_file/dct_level/pre.txt'))
    for path,_,files in pf:
      for filename in files:
        if not filename.split('.')[-1] == 'txt':
            continue
        f = os.path.join(path,filename)
        print('jieba load dict:', f)
        jieba.load_userdict(f)

def test(line,  msgid='1110'):
    url="http://addr.triplet.com.cn/split"
    # url="http://192.168.1.64:7943/split"
    #  url="http://localhost:18888/guizhou/normalization/addr-norm"
    headers = {'content-type': 'application/json',  "Accept": "application/json"}
    body = {
        'messageid': msgid,
        'clientid': "0001",
        'text':[line],
        'encrypt':'false',
    }
    response = requests.post(url,  data = json.dumps(body),  headers = headers)
    # print(response)
    return response.text

def kv(k):
    if k == '省':
        return 'sheng'
    elif k == '市':
        return 'shi'
    elif k == '区':
        return 'qu'
    elif k == '社区':
        return 'shequ'
    elif k == '村居委会':
        return 'cunjuweihui'
    elif k == '街路巷名':
        return 'jieluxiang'
    elif k == '自然村组':
        return 'zirancunzu'
    elif k == '门牌号':
        return 'menpaihao'
    elif k == '小区名':
        return 'xiaoquming'
    elif k == '建筑物名称':
        return 'jianzhuwumingcheng'
    elif k == '组团名称':
        return 'zutuanmingcheng'
    elif k == '栋号':
        return 'donghao'
    elif k == '单元号':
        return 'danyuanhao'
    elif k == '楼层':
        return 'louceng'
    elif k == '户室号':
        return 'hushihao'
    elif k == 'loc':
        return 'nz'
    elif k == '标准地址':
        return 'nz'
    else:
        return 'other'

def file_cut(fnin,  fnout):
    g = open(fnout,  'wb+')
    f = open(fnin,  'r')
    lines = f.readlines()
    import numpy as np
    np.random.shuffle(lines)
    lines = lines
    for line in lines:
        words = jieba.posseg.cut(line)
        strs = ''
        for word in words:
            strs+="%s/%s "%(word.word,  word.flag)
            print(strs)
        strs+="\n"
        g.write(strs.encode('utf-8'))
    g.close()
    f.close()

'''
def file_test(fnin,  fnout):
    g = open(fnout,  'wb+')
    f = open(fnin,  'r')
    lines = f.readlines()
    for line in lines:
        line = line.split(', ')[1]
        itemstrs=[]
        response = test(line)
        lst2d = json.loads(response)['result']
        __lst2d__ = list(jieba.posseg.cut(line))
        default = []
        for __item__ in __lst2d__:
            default.append(1)
            for item in lst2d:
                if item[0] == __item__.word:
                    itemstrs.append('%s/%s ' %(item[0],  kv(item[1])))
                    break
      if len(itemstrs)<len(default):
          itemstrs.append('%s/%s ' %(__item__.word, 'qita'))
          # pdb.set_trace()
          print(''.join(itemstrs))
          g.write(''.join(itemstrs).encode('utf-8'))
          g.close()
          '''

if __name__ == '__main__':
    init_user_dict()
    ls = ['/home/siy/data/zhengzhou_std.csv', '/home/siy/data/广电全量地址_weak.csv']
    for fnin in [ls[-1]]:
        fnout = 'hmm_train_0505.txt'
        file_cut(fnin, fnout)
        # file_cut(fnin,  fnout)


