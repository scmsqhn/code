#!/usr/bin/python
#coding:utf8

'''
Observer
'''

import sys
import os
sys.path.append(os.environ.get('YUNYAN'))
sys.path.append(os.environ.get('WORKBENCH'))
print(os.environ.get('YUNYAN'))
import pdb
import myconfig
import mark_train_data
from mark_train_data import *

def gen(filepath):
    f = open(filepath,'r')
    lines = f.readlines()
    for line in lines:
        yield line

#std_gen = gen(myconfig.STDTXTPATH)

f = open('output.txt','a+')

def compare(base,comp):
    setever = set()
    base_ = gen(base)#myconfig.ZHUJIANPATH)
    for i in base_:
        i = re.sub("[\r\n]","",i)
        value_min = 999999
        match_lst = []
        comp_ = gen(comp)#myconfig.ZHUJIANPATH)
        for j in comp_:
            if value_min < 0.01:
                break
            if (i+j) in setever:
                continue
            j = re.sub("[\r\n]","",j)
            if len(i)<9 or len(j)<9:
                continue
            #if not len(i) > len(j):
            #    i,j = j,i
            data,label,s,r,c = hugry_match(matrix_build_extract(i,j),i,j)
            #s = 100*s/len(j)
            #print(data)
            #print(label)
            print(s,value_min)
            print(match_lst)
            #print(r)
            #print(c)
            #print(i)
            #print(j)
            if s < value_min:
                match_lst = []
                match_lst.append(j)
                value_min = s
            elif s == value_min:
                match_lst.append(j)
            else:
                pass
        #pdb.set_trace()
        for line in match_lst:
            f.write('%s\t%s\t%s\n'%(i,line,s))
            f.flush()
            setever.add(i+line)

compare(myconfig.DONGSTDTXT, myconfig.ZHUJIANPATH)
#compare(myconfig.ZHUJIANPATH, myconfig.DONGSTDTXT)





