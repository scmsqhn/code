# coding:utf-8
import jieba
import os
import pdb
import re
import pandas as pd
import time
import numpy as np
import my_graph

STD_PATH = "/data/network/data/std/zz"
STD_FILE = "dz_zzxx_cs.csv"
TEST_PATH = "/data/network/data/test/zz"

class TrieNode(object):
    def __init__(self,char,node):
        self.data = {}
        self.parent = node
        self.char = char
        self.is_word = False
        self.wealth = 1
        self.hash_set = set()

class Trie(object):
    def __init__(self):
        self.root = TrieNode("ROOT",None)
        self.cursor = []

    def insert_num_lst(self, words, line):
        node = self.root
        for word in words:
            child = node.data.get(word)
            if not child:
                node.data[word] = TrieNode(word,node)
            else:
                node.data[word].wealth += 1
            node = node.data[word]
            node.is_word = True
        node.hash_set.add(line)

    def insert_wd_lst(self, words):
        #print(words)
        node = self.root
        for word in words:
            child = node.data.get(word)
            if not child:
                node.data[word] = TrieNode(word,node)
            else:
                node.data[word].wealth += 1
            node = node.data[word]
        node.is_word = True

    def insert(self, word):
        node = self.root
        for letter in word:
            child = node.data.get(letter)
            if not child:
                node.data[letter] = TrieNode(letter,node)
            else:
                node.data[letter].wealth += 1
            node = node.data[letter]
        node.is_word = True

    def search(self, word):
        node = self.root
        for letter in word:
            node = node.data.get(letter)
            if not node:
                return False
        return node.is_word # 判断单词是否是完整的存在在trie树中

    def get_hash_from_node(self, node, result):
        result.extend(list(node.hash_set))
        for data_item in node.data:
            child = node.data.get(data_item)
            result.extend(list(child.hash_set))
            result = self.get_hash_from_node(child, result)
        return result 

    def search_num_get_node(self, word, result):
        node = self.root
        for letter in word:
            child = node.data.get(letter)
            if not child:
                result.add(node)
                return result
            node = child
            result.add(node) 
        return result

    def scan_child_word(self,node,result):
        node = node
        for letter in node.data:
            child = node.data.get(letter)
            if not child:
                return result
            else:
                if child.is_word == True:
                    result.append(child)
                else:
                    return self.scan_child_word(child,result)
        return result

    def scan_word(self,nodes,words):
        """ get all the node in tree """
        print("scan_word:",[i.char for i in nodes], words)
        _tmp = []
        assert len(nodes)>0
        if len(words)>1 and len(nodes)>0:
            letter,words = words[0],words[1:]
            _tmp = self.scan_many(nodes,letter)
            if len(_tmp) >0:
                return self.scan_word(_tmp, words)
        return nodes
        #print("return 0", nodes)
        #return nodes

    def scan_many(self,lst,letter):
        """scan a lst which contain many node"""
        assert len(lst)>0
        result = []
        for node in lst:
            result = self.scan(node, letter, result)
            #result_combine.extend(result)
        #if len(result) == 0:
        #    print("scan_many 0", lst)
        #    print("sm0",[i.char for i in result])
        #else:
        #    print("scan_many 1", result)
        #    print("sm",[i.char for i in result])
        return result

    def scan(self, node, letter, result):
        """ get all the node in tree """
        if len(node.data)>0:
            if not node.data.get(letter):
                for key in node.data:
                    self.scan(node.data[key], letter, result)
            else:
                node = node.data[letter]
                #self.scan_child_word(node,result)
                result.append(node)
        return result

    def parent_tree(self,node,parstr):
        #print(node.parent.char)
        if node.char == "ROOT":
            #print(parstr[::-1])
            return parstr[::-1]
        else:
            parstr.append(node.parent.char)
            self.parent_tree(node.parent,parstr)

    def starts_with(self, prefix):
        node = self.root
        for letter in prefix:
            node = node.data.get(letter)
            if not node:
                return False
        return True

    def fuzzy_search(self, node, words):
        pass

    def words_route(self,words):
        nodes = [self.root]
        result = []
        result = self.scan_word(nodes,words)
        print(result)
        return result

    def get_start(self, prefix):
        def _get_key(pre, pre_node):
            words_list = []
            if pre_node.is_word:
                words_list.append(pre)
            for x in list(pre_node.data.keys()):
                words_list.extend(_get_key(pre + str(x), pre_node.data.get(x)))
            return words_list
        words = []
        if not self.starts_with(prefix):
           return words
        if self.search(prefix):
            words.append(prefix)
            return words
        node = self.root
        for letter in prefix:
            node = node.data.get(letter)
        return _get_key(prefix, node)

## Your Trie object will be instantiated and called as such:
#addr_tree = Trie()
#dict_tree = Trie()
#
##stand_lines = open(os.path.join(STD_PATH, STD_FILE)).readlines()
#stand_lines = pd.read_csv(os.path.join(STD_PATH, STD_FILE)).iloc[:,1]
#for line in stand_lines:
#    """ insert address into addr_tree """
#    #line_pre = re.split("[\d]",line)[0]
#    #line_num = re.findall("\d+号", line)
#    #if len(line_num)>0:
#    #    line_pre+=line_num[0]
#    #words = list(jieba.cut(line_pre))
#    """ insert all addr_tree """
#    line = strQ2B(line)
#    words = list(jieba.cut(line))
#    addr_tree.insert_wd_lst(words)
#    for word in words:
#        dict_tree.insert(word)
#
#df = pd.DataFrame()
#df['map'] = ""
#df['kw'] = ""
#df['target'] = ""
#
#def check_num(line1, line2):
#    base = ""
#    cont = re.split("\d+",line1)[0]
#    if len(cont)>0:
#        base = list(jieba.cut(cont))[-1]
#    nums1 = re.findall("\d+",line1)
#    nums2 = re.findall("\d+",line2)
#    print(line1, line2)
#    print(nums1, nums2)
#    lmin = min(len(nums1),len(nums2))
#    lmax = max(len(nums1),len(nums2))
#    cnt = 0
#    for i,j in zip(nums1[:lmin], nums2[:lmin]):
#        if i == j:
#            cnt+=1
#            continue
#        break
#    if lmin>0:
#        if not base+nums1[0] in line2:
#            print("False",base+nums1[0])
#            return False
#    if cnt == lmin and cnt>1:
#        return True
#    elif cnt>1:
#        return True
#    else:
#        print("False",nums1, nums2)
#        return False
#
#def check(line1,line2):
#    txts = re.split("\d+",line)
#    if len(txts[0]) < 3:
#        return False
#    nums = re.findall("\d+",line)
#    if len(nums)<1:
#        return False
#    baseline = ""
#    for i in range(2):
#        if i > len(txts)-1:
#            break
#        elif i == 0:
#            baseline+=txts[i][-3:]
#        else:
#            baseline+="\D+"
#        if i > len(nums)-1:
#            break
#        else:
#            baseline+=nums[i]
#    if len(baseline) < 1:
#        return False
#    print(baseline , " weather in ", line2)
#    if len(re.findall(baseline,line2))>0:
#        print(baseline , " bingo in ", line2)
#        print(re.findall(baseline,line2))
#        return True
#    else:
#        return False
#    return False
#
#def _check(line1,line2):
#    txts = re.split("\d+",line)
#    if len(txts[0]) < 2:
#        return False
#    nums = re.findall("\d+",line)
#    if len(nums)<1:
#        return False
#    baseline = ""
#    for i in range(2):
#        if i > len(txts)-1:
#            return baseline
#        elif i == 0:
#            baseline+=txts[i][-3:]
#        else:
#            baseline+=".+?"
#        if i > len(nums)-1:
#            return baseline
#        else:
#            baseline+=nums[i]
#    if len(baseline) < 1:
#        return False
#    if len(re.findall(baseline,line2))>0:
#        print(baseline , " is in ", line2)
#        return True
#    else:
#        print(baseline , " not in ", line2)
#        return False
#
#input_file = []
#cnt=0
#for _,_,docs in os.walk(TEST_PATH):
#    for doc in docs:
#        lines = pd.read_csv(os.path.join(TEST_PATH, doc)).iloc[:,1]
#        #lines = open(os.path.join(TEST_PATH,doc)).readlines()[:1000]
#        lines = [lines[np.random.randint(len(lines))] for i in range(300)]
#        for line in lines:
#            line = re.sub("[\r\n]","",str(line))
#            line = strQ2B(line)
#            res = []
#            """ 使用第一个数字前的文本进行分词 """
#            line_pre = re.split("[\d+]",line)[0]
#            #line_num = re.findall("\d+号", line)
#            #if len(line_num)>0:
#            #    line_pre+=line_num[0]
#            #for word in jieba.cut(line_pre):
#            """ 文本进行分词 """
#            for word in jieba.cut(line_pre):
#                if dict_tree.search(word):
#                    res.append(word)
#            if cnt%1000 == 1:
#                print(cnt, time.time())
#            #if len(res) < 4:
#            #    continue
#            #    result = []
#            #    df.loc[str(cnt),'map'] = line
#            #    df.loc[str(cnt),'target'] = ""
#            #    df.loc[str(cnt),'kw'] = ",".join(res)
#            if True:#else:
#                result = addr_tree.words_route(res)
#                #print(res,result)
#                if len(result) == 0:
#                    df.loc[str(cnt),'map'] = line
#                    df.loc[str(cnt),'target'] = "".join([])
#                    df.loc[str(cnt),'kw'] = ",".join(res)
#                    cnt+=1
#                    continue
#                flag = False
#                for i in result:
#                  node_res = []
#                  node_res = addr_tree.scan_child_word(i,node_res)
#                  for node in node_res:
#                    #print(res, i.char)
#                    parent_res = []
#                    addr_tree.parent_tree(node,parent_res)
#                    print(res,parent_res)
#                    if check_num(line, "".join(parent_res[::-1])):
#                        df.loc[str(cnt),'map'] = line
#                        df.loc[str(cnt),'target'] = "".join(parent_res[::-1])
#                        df.loc[str(cnt),'kw'] = ",".join(res)
#                        flag == True
#                        cnt+=1
#                if flag == False:
#                    df.loc[str(cnt),'map'] = line
#                    df.loc[str(cnt),'target'] = "".join([])
#                    df.loc[str(cnt),'kw'] = ",".join(res)
#                    cnt+=1
#        df.to_csv("./record.csv")
###        print(cnt, 'save')
