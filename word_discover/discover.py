#!encoding=utf-8
#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: discover.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-13
#   describe:
#================================================================

from collections import defaultdict
import numpy as np
import pdb
import traceback
import re
import os

import sys


lenth_line = 100000
inf = sys.argv[1]
outf = sys.argv[2]


def gen():
    lines = open(inf,'r').readlines()
    #lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
    np.random.shuffle(lines)
    for line in lines[:lenth_line]:
        line.strip()
        if len(line) == 0:
            continue
        yield line


texts = gen


from collections import defaultdict
import numpy as np


n = 5
min_count = 10
ngrams = defaultdict(int)

for t in texts():
    for i in range(len(t)):
        for j in range(1, n+1):
            if i+j <= len(t):
                ngrams[t[i:i+j]] += 1

ngrams = {i:j for i,j in ngrams.items() if j >= min_count}
total = 1.*sum([j for i,j in ngrams.items() if len(i) == 1])


#pdb.set_trace()

min_proba = {2:5, 3:25, 4:125}


# 计算凝固度
def is_keep(s, min_proba):
    if len(s) >= 2:
        score = min([total*ngrams[s]/(ngrams[s[:i+1]]*ngrams[s[i+1:]]) for i in range(len(s)-1)])
        if score > min_proba[len(s)]:
            return True
    else:
        return False

ngrams_ = set(i for i,j in ngrams.items() if is_keep(i, min_proba))

def cut(s):
    #pdb.set_trace()
    r = np.array([0]*(len(s)-1))
    for i in range(len(s)-1):
        for j in range(2, n+1):
            if s[i:i+j] in ngrams_:
                r[i:i+j-1] += 1
                #pdb.set_trace()
    w = [s[0]]
    for i in range(1, len(s)):
        if r[i-1] > 0:
            w[-1] += s[i]
        else:
            w.append(s[i])
    return combine(w)

gg = open('dict.txt','a+')

def combine(w):
    res = []
    res.append(w[0])
    for c in w[1:]:
        if len(c) == 1:
            res[-1]+=c
        else:
            res.append(c)
            gg.write("%s\n"%c)
    # print(res)
    print([item[::-1] for item in res[::-1]])
    return [item for item in res[::-1]]

g = open(outf,'w+')

words = defaultdict(int)
for t in texts():
    for i in cut(t):
        i.strip()
        i = re.sub("[\r\n]", "", i)
        g.write(i+'\n')
        #print(i)
        words[i] += 1
g.close()
gg.close()

words = {i:j for i,j in words.items() if j >= min_count}


def is_real(s):
    if len(s) >= 3:
        for i in range(3, n+1):
            for j in range(len(s)-i+1):
                if s[j:j+i] not in ngrams_:
                    return False
        return True
    else:
        return True

w = {i:j for i,j in words.items() if is_real(i)}

print(w)



