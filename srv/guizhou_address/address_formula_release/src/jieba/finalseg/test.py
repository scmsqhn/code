import jieba
import re
import pdb
jieba.load_userdict("dict_nz.txt")
#jieba.load_userdict("guiyang_baidu_addr_split.txt")
cnt = 0
g = open("output.txt","a+")
with open("name.txt","r") as f:
    lines = f.readlines()
    for line in lines:
        cnt+=1
        g.write("%s\n"%str(list(jieba.cut(line))))
        if cnt%100 == 0:
            print(list(jieba.cut(line)))
with open("address.txt","r") as f:
    lines = f.readlines()
    for line in lines:
        cnt+=1
        g.write("%s\n"%str(list(jieba.cut(line))))
        if cnt%100 == 0:
            print(list(jieba.cut(line)))

