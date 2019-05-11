#!coding=utf8
import xlrd
from scipy.optimize import linear_sum_assignment
import numpy as np
import pandas as pd
import pdb
import sys
#import xlrd
#import jsonload
#from jsonload import get_kv,loadFont,cal_dis
from function_ultra import utils
from function_ultra.mylog import logger
import time
import codecs

logger.debug("> start mark")
labelmap = {}
labelmap["B"] = 0
labelmap["I"] = 1
labelmap["O"] = 2
labelmap["S"] = 3

def cost_matrix_value(cost):
    row_ind,col_ind=linear_sum_assignment(cost)
    #print(row_ind)#开销矩阵对应的行索引
    #print(col_ind)#对应行索引的最优指派的列索引
    #print(cost[row_ind,col_ind])#提取每个行索引的最优指派列索引所在的元素，形成数组
    #print(cost[row_ind,col_ind].sum())#数组求和
    return cost[row_ind,col_ind].sum(),row_ind,col_ind
#for i,j in zip(row_ind, col_ind):
#    print(cost[i,j])


def matrix_build_extract(contl,contr,dct=None,weight=0):
    #ichar_num = ["一","二","三","四","五","六","七","八","九","零"]
    #ichar_num.extend(["栋","单元","层","号","室","户"])
    ichar_num = [" "]
    #pdb.set_trace()
    mat = np.array([1]*len(contl)*len(contr)).reshape(len(contl),len(contr))
    #mulby= (len(contl)-len(contr))**2
    #mulby+=2
    mulby=1
    for i in range(len(contl)):
        ll=1+len(contl)-i
        for j in range(len(contr)):
            lr=1+len(contr)-j
            #if not dct.get('%s_%s'%(contl[i],contr[j]),-1) == -1:
            #    mat[i][j]=0
            #if contl[i] in ichar_num or contr[j] in ichar_num:
            #    mulby=0
            #    mulby=0
            #if False:
            #    pass
                #pdb.set_trace()
                #mat[i][j]=(1/len(contl))
            #    mat[i][j]=0
            if contl[i]==contr[j]:
                mat[i][j]=0
            else:
                if weight==1:#前面重要
                    #mat[i][j]=1*mulby
                    mat[i][j]=(ll+lr)*mulby
                elif weight==-1:#后重要
                    mat[i][j]=(i+j)*mulby
                    #mat[i][j]=(lr*ll*mulby)
                    #mat[i][j]=np.log(10+(lr*ll*mulby))
                elif weight==0:
                    mat[i][j]=mulby
                else:
                    logger.log("there is sth wrong")
                    pdb.set_trace()
            assert lr>0
            assert ll>0
    return mat

def matrix_build(contl,contr,dct=None,weight=0):
    ichar_num = [" "]
    mat = np.array([1]*len(contl)*len(contr)).reshape(len(contl),len(contr))
    mulby=1
    for i in range(len(contl)):
        ll=1+len(contl)-i
        for j in range(len(contr)):
            lr=1+len(contr)-j
            if not dct.get('%s_%s'%(contl[i],contr[j]),-1) == -1:
                mat[i][j]=0
            else:
                if weight==1:#前面重要
                    mat[i][j]=(ll+lr)*mulby
                elif weight==-1:#后重要
                    mat[i][j]=(i+j)*mulby
                elif weight==0:
                    mat[i][j]=mulby
                else:
                    logger.log("there is sth wrong")
                    pdb.set_trace()
            assert lr>0
            assert ll>0
    return mat

def hugry_match(mat,k1s,k2s):
    s,r,c = cost_matrix_value(mat)
    data = []
    label = []
    match = []
    for i,j in zip(r,c):
        if k1s[i]==k2s[j]:
            match.append(j)
        else:
            pass
    for i in range(len(k2s)):
        if i in match:
            data.append(k2s[i])
            label.append(labelmap["I"])
        else:
            data.append(k2s[i])
            label.append(labelmap["O"])
    return data,label,s,r,c

def read_txt(filename,shuffle):
    lines = codecs.open(filename,"r","utf-8").readlines()
    for line in lines:
        if shuffle:
            line = lines[np.random.randint(len(lines))]
        line = line.split("&")[0]
        line = utils.clr(line)
        yield line

'''
def mark_from_txt_compare(filename):
    gen = read_txt(filename)
    _gen = read_txt(filename)
    for i in gen:
        for j in _gen:
            if i == j:
                continue
            elif len(i)>len(j):
                data, label,s,r,c = hugry_match(matrix_build(i,j),i,j)
                yield (data,label)
            else:
                data, label,s,r,c = hugry_match(matrix_build(j,i),j,i)
                yield (data,label)
'''
def show_match(filename):
    cnt = 100
    with open("match_sample.txt","r") as f:
        lines = f.readlines()
        for line in lines:
            kv = line.split("\t")
            pas = ""
            for i,j in zip(kv[0],kv[1]):
                if j == "1":
                    pas+=i
                else:
                    pas+="_"
                    cnt-=1
                    if cnt<0:
                        time.sleep(0.2)
                        cnt=100

def read_xlrd(filename):
    ad = xlrd.open_workbook(filename)
    sts = ad.sheets()
    rows = sts[0].get_rows()
    result = []
    for line in rows:
        k = line[14].value
        v = line[10].value
        k = utils.clr(k)
        v = utils.clr(v)
        data,label,s,r,c= hugry_match(matrix_build(k,v),k,v)
        yield (data,label,k,v)

def addr_classifier(k,v,dct,direct):
    data,label,s,r,c= hugry_match(matrix_build(k,v,dct,direct),k,v)
    return data,label,s,r,c

def init_ner_train_data(filename):
    gen = read_txt(filename,shuffle=True)
    f = open(filename,"a+")
    for sent in gen:
        sent = utils.clr(sent)
        for char in sent:
            f.write("%s O\n"%char)
        f.write("\n")
    f.close()

def sent_pair_gen(filename):
    with open(filename, "a+") as gh:
        gen = read_xlrd("/home/dell/data/addr_guiyang_zhongtian_huayuan.xlsx")
        for i in gen:
            k = i[2]
            v = i[3]
            gh.write("%s %s\n"%(k,v))
            gh.flush()
import re

def seperate_zhengz_address(filename):
    rt = open("/home/dell/data/zhengz_train.txt","w+")
    wx = open("/home/dell/data/zhengz_dev.txt","w+")
    tmp = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = re.sub("[\r\n]","",line)
            line = re.sub("NONE","",line)
            line = re.sub(" ","",line)
            line = utils.clr(line)
            if 'ROOT' in line:
                qua,ans = line.split('ROOT')
                rt.write("%s %s 0\n"%(qua,ans))
            else:
                if len(tmp) == 2:
                    rt.write("%s %s 1\n"%(tmp[0],tmp[1]))
                    tmp = []
                else:
                    tmp.append(line)
    rt.close()
    wx.close()


def zhengz_train_data_gen_sent_pairs():
    standf = '/home/dell/data/zz_std_words.txt'
    samplef = '/home/dell/data/eval_zz.txt'
    filename = "/home/dell/data/zhengz_comp.txt"
    stand = read_txt(standf,shuffle=True)
    sampl = read_txt(samplef,shuffle=True)
    cont = open(filename,"w+")
    index = 0
    for lstd in stand:
        for lsam in sampl:
            cont.write('%s %s\n'%(lstd,lsam))
            index+=1
            if index>1000000:
                break
    stand.close()
    sampl.close()
    cont.close()

def train_data_gen_sent_pairs(filename,writeintrain,writeintest):
    with open(writeintrain,"w+") as g:
     with open(writeintest,"w+") as h:
      with open(filename,"r") as f:
        lines = f.readlines()
        sep = int(len(lines)*0.9//1)
        for line in lines[:sep]:
            line = re.sub("[\r\n]","",line)
            sent_a, sent_b = line.split(" ")
            g.write("%s %s 0\n"%(sent_a,sent_b))
            cnt = np.random.randint(len(lines))
            g.write("%s %s 1\n"%(sent_a,lines[cnt].split(" ")[1]))
            cnt = np.random.randint(len(lines))
            g.write("%s %s 1\n"%(sent_a,lines[cnt].split(" ")[1]))
            cnt = np.random.randint(len(lines))
            g.write("%s %s 1\n"%(sent_a,lines[cnt].split(" ")[1]))

        for line in lines[sep:]:
            line = re.sub("[\r\n]","",line)
            sent_a, sent_b = line.split(" ")
            h.write("%s %s 0\n"%(sent_a,sent_b))
            cnt = np.random.randint(len(lines))
            h.write("%s %s 1\n"%(sent_a,lines[cnt].split(" ")[1]))
            cnt = np.random.randint(len(lines))
            h.write("%s %s 1\n"%(sent_a,lines[cnt].split(" ")[1]))
            cnt = np.random.randint(len(lines))
            h.write("%s %s 1\n"%(sent_a,lines[cnt].split(" ")[1]))



if __name__ == "__main__":
    #sent_pair_gen("./sent_pair_word.txt")
    #zhengz_train_data_gen_sent_pairs()
    #pdb.set_trace()
    #seperate_zhengz_address("/home/dell/data/output_zz.txt")

    #train_data_gen_sent_pairs("/home/dell/data/sent_pair_word.txt","/home/dell/data/example_train_sentpair_zhongtianhuayuan", \
    #"/home/dell/data/example_test_sentpair_zhongtianhuayuan")
    #gen = read_xlrd("data/addr_guiyang_zhongtian_huayuan.xlsx")
    #for i in gen:
    #    print(i)
    #filename = sys.argv[1]
    #init_ner_train_data(filename)
    with open("match_sample_reverse.txt","a+") as gh:
        #gen = mark_from_txt_compare("/data/network_zz/output/doc_pre_handle.txt")
        gen = read_xlrd("/home/dell/data/addr_guiyang_zhongtian_huayuan.xlsx")
        print(gen)
        for i in gen:
            print(i)
            k = "".join(i[0])
            v = "".join([str(_) for _ in i[1]])
            for ii,jj in zip(k,v):
                gh.write("%s %s\n"%(ii,jj))
            gh.write("\n")
            gh.flush()
                #if "1" in "".join([str(_) for _ in i[1]]):
                #    pdb.set_trace()

