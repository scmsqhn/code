#!encoding:utf-8

import mylog
from mylog import logger
import collections
import numpy as np
import pandas as pd
import jieba
import os
import pdb
import re
import pandas as pd
import time
import numpy as np
import my_graph
import trie_tree
from trie_tree import TrieNode
from trie_tree import Trie
import utils
from utils import strQ2B
import pickle_helper
import networkx as nx
import time
#import mtmw
#from mtmw import tasks

#STD_PATH = "/data/network/data/std/zz"
STD_PATH = "/data/network_gy/data/std"
STD_FILE = "standard_address_guiyang3.txt"
#STD_FILE = "dz_zzxx_cs.csv"
TEST_PATH = "/data/network_gy/data/test/gy"
#TEST_PATH = "/data/network/data/test/zz"
SAVE_PATH = "/data/network_gy"
SAVE_FILE = "pickle_gy.txt"
FLAG_INIT_MODEL = False
#FLAG_INIT_MODEL = True
#FLAG_LOAD_MODEL = False
FLAG_LOAD_MODEL = True



class Address_Acti(object):

    def __init__(self):
        self.batch = 10000
        self.test_batch = 100
        if FLAG_INIT_MODEL:
            self.addr_tree = Trie()
            self.dict_tree = Trie()
            self.num_tree = Trie()
            #self.init_num_hash()
            self.graph = my_graph.My_Graph()
            self.init_model()
            print("init_model ok")
            pickle_helper.save(os.path.join(SAVE_PATH,SAVE_FILE),[self.addr_tree,self.dict_tree,self.graph,self.num_tree])
            print("pickle save ok")
        if FLAG_LOAD_MODEL:
            self.addr_tree, self.dict_tree, self.graph,self.num_tree = pickle_helper.load(os.path.join(SAVE_PATH,SAVE_FILE),[1,2,3,4])
            print("pickle load ok")

    def minEditDist(self, sm, sn):
        m,n = len(sm)+1, len(sn)+1
        matrix = [[0]*n for i in range(m)]
        matrix[0][0] = 0
        for i in range(1,m):
            matrix[i][0] = matrix[i-1][0] + 1
        for j in range(1,n):
            matrix[0][j] = matrix[0][j-1] + 1
        const = 0
        for i in range(1,m):
            for j in range(1,n):
                if sm[i-1] == sn[j-1]:
                    cost = 0
                else:
                    cost = 1
                matrix[i][j] = min(matrix[i-1][j]+1,matrix[i][j-1]+1,matrix[i-1][j-1]+cost)
        return matrix[m-1][n-1]

    def cut_filter(self,src_sent):
        cmdin = r"区.+?与.+?交叉口[向东]?[\d+米]?路?[东南西北]?"

    def init_num_hash(self):
        stand_lines = open(os.path.join(STD_PATH, STD_FILE)).readlines()
        for line in stand_lines:
            """ insert address into addr_tree """
            """ insert all addr_tree """
            line = utils.clr(line)
            nums = list(re.findall("\d+",line))
            self.num_tree.insert_num_lst(nums,hash(line))

    def init_model(self):
        stand_lines = open(os.path.join(STD_PATH, STD_FILE)).readlines()
        #stand_lines = pd.read_csv(os.path.join(STD_PATH, STD_FILE)).iloc[:,1]
        #stand_lines = [stand_lines[np.random.randint(len(stand_lines))] for i in range(self.batch)]
        for line in stand_lines:
            """ insert address into addr_tree """
            """ insert all addr_tree """
            line = utils.clr(line)
            words = list(jieba.cut(line))
            nums = list(re.findall("\d+",line))
            self.num_tree.insert_num_lst(nums,hash(line))
            self.addr_tree.insert_wd_lst(words)
            for word in words:
                self.dict_tree.insert(word)

    def score_num_lst(self, nums1, nums2):
        if "" in nums1:
            nums1.remove("")
        if "" in nums2:
            nums2.remove("")
        """ use num to check weather same or not """
        lmin = min(len(nums1),len(nums2))
        #lmax = max(len(nums1),len(nums2))
        cnt = 0
        for i,j in zip(nums1[:lmin], nums2[:lmin]):
            print(i,j)
            if i == j:
                cnt+=1
                continue
            break
        if cnt == lmin and cnt>0:
            print(nums1 , " equal " ,nums2)
            return (cnt/lmin)*100
        elif cnt>0:
            print(nums1 , " equal " ,nums2)
            return (cnt/lmin)*100
        else:
            print(nums1, " not equal ", nums2)
            return 0.0

    def check_num_lst(self, nums1, nums2):
        if "" in nums1:
            nums1.remove("")
        if "" in nums2:
            nums2.remove("")
        """ use num to check weather same or not """
        lmin = min(len(nums1),len(nums2))
        #lmax = max(len(nums1),len(nums2))
        cnt = 0
        for i,j in zip(nums1[:lmin], nums2[:lmin]):
            print(i,j)
            if i == j:
                cnt+=1
                continue
            break
        if cnt == lmin and cnt>0:
            print(nums1 , " equal " ,nums2)
            return True
        elif cnt>1:
            print(nums1 , " equal " ,nums2)
            return True
        else:
            print(nums1, " not equal ", nums2)
            return False

    def check_num(self, line1, line2):
        """ use num to check weather same or not """
        print("判断数字是否一致", line1,line2)
        cont = re.split("\d+",line1)[0]
        base = ""
        if len(cont)>0:
            #base = list(jieba.cut(cont))[-1]
            base = cont[-3:]
        nums1 = re.findall("\d+",line1)
        nums2 = re.findall("\d+",line2)
        print(line1, line2)
        print(nums1, nums2)
        lmin = min(len(nums1),len(nums2))
        #lmax = max(len(nums1),len(nums2))
        cnt = 0
        for i,j in zip(nums1[:lmin], nums2[:lmin]):
            print(i,j)
            if i == j:
                cnt+=1
                continue
            break
        if lmin>0:
            if not base+nums1[0] in line2:
                print("False",line1, line2)
                return False
        if cnt == lmin and cnt>0:
            return True
        elif cnt>0:
            return True
        else:
            print("False",line1, line2)
            return False

    def _check_num(self, line1, line2):
        """ use num to check weather same or not """
        base = ""
        cont = re.split("\d+",line1)[0]
        if len(cont)>0:
            #base = list(jieba.cut(cont))[-1]
            base = cont[-3:]
        nums1 = re.findall("\d+",line1)
        nums2 = re.findall("\d+",line2)
        print(line1, line2)
        print(nums1, nums2)
        lmin = min(len(nums1),len(nums2))
        #lmax = max(len(nums1),len(nums2))
        cnt = 0
        for i,j in zip(nums1[:lmin], nums2[:lmin]):
            if i == j:
                cnt+=1
                continue
            break
        if lmin>0:
            if not base+nums1[0] in line2:
                print("False",base+nums1[0])
                return False
        if cnt == lmin and cnt>0:
            return True
        elif cnt>1:
            return True
        else:
            print("False",nums1, nums2)
            return False
    
    def check(self,line1,line2):
        txts = re.split("\d+",line)
        if len(txts[0]) < 2:
            return False
        nums = re.findall("\d+",line)
        if len(nums)<1:
            return False
        baseline = ""
        for i in range(2):
            if i > len(txts)-1:
                break
            elif i == 0:
                baseline+=txts[i][-3:]
            else:
                baseline+="\D+"
            if i > len(nums)-1:
                break
            else:
                baseline+=nums[i]
        if len(baseline) < 1:
            return False
        print(baseline , " weather in ", line2)
        if len(re.findall(baseline,line2))>0:
            print(baseline , " bingo in ", line2)
            print(re.findall(baseline,line2))
            return True
        else:
            return False
        return False
    
    def _check(self,line1,line2):
        txts = re.split("\d+",line)
        if len(txts[0]) < 2:
            return False
        nums = re.findall("\d+",line)
        if len(nums)<1:
            return False
        baseline = ""
        for i in range(2):
            if i > len(txts)-1:
                return baseline
            elif i == 0:
                baseline+=txts[i][-3:]
            else:
                baseline+=".+?"
            if i > len(nums)-1:
                return baseline
            else:
                baseline+=nums[i]
        if len(baseline) < 1:
            return False
        if len(re.findall(baseline,line2))>0:
            print(baseline , " is in ", line2)
            return True
        else:
            print(baseline , " not in ", line2)
            return False

    def word_filter(self, line_pre):
        res = []
        for word in jieba.cut(line_pre):
            if self.dict_tree.search(word):
                res.append(word)
        return res
    
    def common_nbs(self,comm_nbs):
        result = set()
        if len(comm_nbs)>1:
            result  = set(comm_nbs[0])
            for i in comm_nbs[1:]:
                if len(result & set(i))>0:
                    print("交集", len(result), len(set(i)))
                    result = result & set(i)
                    print(self.graph.sent[list(result)[0]])
                else:
                    return result
        elif len(comm_nbs)==1:
            result = comm_nbs[0]
        if len(result)>0:
            print("最终输出过滤后的标准地址", self.graph.sent[list(result)[0]])
        return result

    def _check_num(self, line1, line2):
        """ use num to check weather same or not """
        base = ""
        cont = re.split("\d+",line1)[0]
        if len(cont)>0:
            #base = list(jieba.cut(cont))[-1]
            base = cont[-3:]
        nums1 = re.findall("\d+",line1)
        nums2 = re.findall("\d+",line2)
        print(line1, line2)
        print(nums1, nums2)
        lmin = min(len(nums1),len(nums2))
        #lmax = max(len(nums1),len(nums2))
        cnt = 0
        for i,j in zip(nums1[:lmin], nums2[:lmin]):
            if i == j:
                cnt+=1
                continue
            break
        if lmin>0:
            if not base+nums1[0] in line2:
                print("False",base+nums1[0])
                return False
        if cnt == lmin and cnt>0:
            return True
        elif cnt>1:
            return True
        else:
            print("False",nums1, nums2)
            return False
    
    def check(self,line1,line2):
        txts = re.split("\d+",line)
        if len(txts[0]) < 2:
            return False
        nums = re.findall("\d+",line)
        if len(nums)<1:
            return False
        baseline = ""
        for i in range(2):
            if i > len(txts)-1:
                break
            elif i == 0:
                baseline+=txts[i][-3:]
            else:
                baseline+="\D+"
            if i > len(nums)-1:
                break
            else:
                baseline+=nums[i]
        if len(baseline) < 1:
            return False
        print(baseline , " weather in ", line2)
        if len(re.findall(baseline,line2))>0:
            print(baseline , " bingo in ", line2)
            print(re.findall(baseline,line2))
            return True
        else:
            return False
        return False
    
    def _check(self,line1,line2):
        txts = re.split("\d+",line)
        if len(txts[0]) < 2:
            return False
        nums = re.findall("\d+",line)
        if len(nums)<1:
            return False
        baseline = ""
        for i in range(2):
            if i > len(txts)-1:
                return baseline
            elif i == 0:
                baseline+=txts[i][-3:]
            else:
                baseline+=".+?"
            if i > len(nums)-1:
                return baseline
            else:
                baseline+=nums[i]
        if len(baseline) < 1:
            return False
        if len(re.findall(baseline,line2))>0:
            print(baseline , " is in ", line2)
            return True
        else:
            print(baseline , " not in ", line2)
            return False
    
    def _query_one(self, line):
        output,res,score = [],[],[]
        min_edit_value = 9999 
        parts = re.split("\d+",line)
        my_txt = utils.without_num(line)
        my_num = re.findall("\d+",line)
        result,res = self.route_text(my_txt,my_num)
        print("句子集合数目", len(result), "关键词集合", res)
        return result, res, 0

    def editDist(self, line, result):
        """get the minist edit distance of line with result"""
        min_edit_value = 999
        minist_one = ""
        for hs in list(result):
            standard_addr = self.graph.sent[hs]
            print("比较数字部分文本", utils.get_nums(line), utils.get_nums(standard_addr))
            v = self.minEditDist(utils.get_nums(line), utils.get_nums(standard_addr))
            if v < min_edit_value:
                minist_one = hs
                min_edit_value = v
        return minist_one

    def route_text(self,line,lst):
        print("过滤掉无用文本 ", line,lst)
        line = utils.clr(str(line))
        #line_pre = utils.before_first_num(line)
        res = self.word_filter(line)
        print("经过过滤的词条",res)
        #res.extend(lst)
        words_route = []
        comm_nbs = []
        if len(res) == 1:
            res.extend(res)
        for i in range(len(res)-1):
            print(res)
            try:
                #conn = nx.all_shortest_paths(self.graph.tree_di,res[i],res[i+1])
                p_node = res[i]
                a_node = res[i+1]
                if len(words_route) == 0:
                   words_route.append(p_node)
                try:
                    route = nx.shortest_path(self.graph.tree_di,words_route[-1],a_node)
                    print('是否存在最短路径 ', route)
                    words_route.append(a_node)
                    print("add node", i, a_node)
                    #weight = self.graph.tree_di[words_route[-1]][a_node]['weight']
                    #weight = self.graph.tree_di[words_route[-1]][a_node]['weight']
                except:
                    print("not connect direct, continue, find the next one, utile to the head of words lst")
                    print("过滤复杂文本的词条")
                    #words_route = words_route[:-1]
                    #words_route.append(a_node)
                    continue
            except:
                print("networkx error")
                continue
        #words_route = words_route[::-1]
        print("复杂文本", res)
        print("过滤输出", words_route)
        if " " in words_route:
            words_route.remove(" ")
        if len(words_route)>0:
            words_route.insert(0,words_route[0])
        for i in range(len(words_route)):
            try:
                comm_nbs.extend(list(nx.all_neighbors(self.graph.di,words_route[i])))
            except:
                print("添加邻居出错")
        print("所有的邻居都添加到列表中,等待计算")
        print("列表中共有多少个item", len(comm_nbs))
        cnt_lst = collections.Counter(comm_nbs)
        sorted_lst = sorted(cnt_lst.items(), key = lambda d:d[1], reverse=True)
        if not len(sorted_lst)>0:
            return [],words_route
        max_value = sorted_lst[0][1]
        #result = self.common_nbs(comm_nbs)
        #result = self.common_nbs(comm_nbs)
        result = filter(lambda x:utils.is_max(x,max_value),sorted_lst)
        result = [i[0] for i in result]
        print("一共有多少个句子", len(result))
        print("公共邻居最多的句子", self.graph.sent[result[0]])
        print("公共邻居最少的句子", self.graph.sent[result[-1]])
        print("最终关键词", words_route)
        return result,words_route

    def format_txt(self, txts):
        """ date 1114 """ 
        _txts_res = ""
        for txt in txts:
            txt = re.sub("号楼","号",txt)
            txt = re.sub("号院","号",txt)
            txt = re.sub("附(\d+)号","\1号",txt)
            _txts_res+=txt
        return re.findall("[\dA-Za-z]+",_txts_res)

    def handle_num(self, line):
        nums = re.split("[^0-9a-zA-Z]+",line)
        #txts = re.split("[0-9a-zA-Z]",line)
        #_txts = self.format_txt(txts)
        #output = []
        #for i,j in zip(nums,_txts):
        #    output.append(i)
        #    output.append(j)
        #return output
        return nums

    def save_one(self,line,target,f):
        f.write("%s,%s\n"%(line, "ROOT"+target))

    def save_one_txt(self,result,res,score,line,f):
        if len(result) == 0:
            f.write("%s,%s\n"%(line, "None"))
            return 
        for parent_res in result:
            f.write("%s,%s\n"%(line, "ROOT"+self.graph.sent[parent_res]))
        
def main():
    filename = './output/output_1116.txt'
    df = pd.DataFrame()
    #df['map'] = ""
    #df['kw'] = ""
    #df['target'] = ""
    #df['score'] = ""
    #ans = input("please input the address ")
    #print(address_activity.query_line(ans))
    lines = open("./data/test/gy/eval_guiyang.txt","r").readlines()
    #lines = open("./data/test/gy/guiyang_20k.txt","r").readlines()
    #lines = open("./data/test/gy/xiaoqu_zutuan.txt","r").readlines()
    with open(filename,"a+") as f:
        for line in lines[1:]:
            print(line)
            output, res, score = address_activity._query_one(line)
            if len(output) == 0:
                address_activity.save_one(line, "None", f)
            else:
                target = address_activity.editDist(line, output)
                address_activity.save_one(line, address_activity.graph.sent[target], f)

if __name__ == "__main__":
    address_activity = Address_Acti()
    while(1):
        main()

