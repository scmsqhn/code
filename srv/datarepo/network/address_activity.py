# coding:utf-8

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
import tasks

#STD_PATH = "/data/network/data/std/zz"
STD_PATH = "/data/network/data/std"
STD_FILE = "gy_std_addr3.txt"
#STD_FILE = "dz_zzxx_cs.csv"
TEST_PATH = "/data/network/data/test/gy"
SAVE_PATH = "/data/network"
SAVE_FILE = "pickle_gz.txt"
#FLAG_INIT_MODEL = False
FLAG_INIT_MODEL = True
FLAG_SAVE_MODEL = False
FLAG_LOAD_MODEL = False



class Address_Acti(object):

    def __init__(self):
        self.batch = 6000000
        self.test_batch = 300
        if FLAG_INIT_MODEL:
            self.addr_tree = Trie()
            self.dict_tree = Trie()
            self.graph = my_graph.My_Graph()
            self.init_model()
            print("init_model ok")
            pickle_helper.save(os.path.join(SAVE_PATH,SAVE_FILE),[self.addr_tree,self.dict_tree,self.graph])
            print("pickle save ok")
        if FLAG_LOAD_MODEL:
            self.addr_tree, self.dict_tree, self.graph = pickle_helper.load(os.path.join(SAVE_PATH,SAVE_FILE),[1,2,3])
            print("pickle load ok")

    def init_model(self):
        stand_lines = open(os.path.join(STD_PATH, STD_FILE)).readlines()
        #stand_lines = pd.read_csv(os.path.join(STD_PATH, STD_FILE)).iloc[:,1]
        stand_lines = [stand_lines[np.random.randint(len(stand_lines))] for i in range(self.batch)]
        for line in stand_lines:
            """ insert address into addr_tree """
            """ insert all addr_tree """
            line = utils.clr(line)
            words = list(jieba.cut(line))
            self.addr_tree.insert_wd_lst(words)
            for word in words:
                self.dict_tree.insert(word)

    def check_num_lst(self, nums1, nums2):
        nums1.remove("")
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
        elif cnt>0:
            print(nums1 , " equal " ,nums2)
            return True
        else:
            print(nums1, " not equal ", nums2)
            return False

    def check_num(self, line1, line2):
        """ use num to check weather same or not """
        print(line1,line2)
        pdb.set_trace()
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

    """
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
    """

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
                    result = result & set(i)
                else:
                    return result
        elif len(comm_nbs)==1:
            result = comm_nbs[0]
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

    """

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

    """
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
                    result = result & set(i)
                else:
                    return result
        elif len(comm_nbs)==1:
            result = comm_nbs[0]
        return result

    def _query_one(self, line):
        output,res = [],[]
        parts = re.split("[\da-zA-Z]+",line)
        if len(parts)>1:

            #result,res = tasks.handle_text.delay(parts[0])
            result,res = self.handle_text(parts[0])
            for hs in result:
                try:
                    self.graph.sent[hs]
                except:
                    continue
                _line = self.graph.sent[hs]
                _parts = re.split("[\da-zA-Z]+",line)
                __line = re.split("[^\da-zA-Z]+",_line)
                nums = re.split("[^\da-zA-Z]+",line)
                #nums = self.handle_num(line[len(parts[0]):])
                #nums = tasks.handle_num(line[len(parts[0]):])
                if True == self.check_num_lst(__line ,nums):
                    if "".join(res)[-2:] == __line[0][-2:]:
                        output.append(_line)
                    else:
                        print("".join(res)[-3:] ," not equal ", _parts[0][-3:])
        return output,res

    def handle_text(self,line):
        line = utils.clr(str(line))
        line_pre = utils.before_first_num(line)
        res = self.word_filter(line_pre)
        comm_nbs = []
        for i in range(len(res)-2):
            print(res)
            try:
                #conn = nx.all_shortest_paths(self.graph.tree_di,res[i],res[i+1])
                comm_nbs.append(list(nx.common_neighbors(self.graph.di,res[i],res[i+1])))
            except:
                print("networkx error")
                continue
            #conn = nx.all_shortest_paths(self.graph.tree_di,res[i],res[i+1])
            comm_nbs.append(list(nx.common_neighbors(self.graph.di,res[i],res[i+1])))
        result = self.common_nbs(comm_nbs)
        return result,res

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

    def query_one(self, line):
        line = utils.clr(str(line))
        line_pre = utils.before_first_num(line)
        #fir_num= utils.first_numbers(line)
        res = self.word_filter(line_pre)
        res.extend(utils.numbers(line))
        comm_nbs = []
        for i in range(len(res)-1):
            print(res)
            try:
                #conn = nx.all_shortest_paths(self.graph.tree_di,res[i],res[i+1])
                comm_nbs.append(list(nx.common_neighbors(self.graph.di,res[i],res[i+1])))
            except:
                print("networkx error")
                continue
            #conn = nx.all_shortest_paths(self.graph.tree_di,res[i],res[i+1])
            comm_nbs.append(list(nx.common_neighbors(self.graph.di,res[i],res[i+1])))
        result = self.common_nbs(comm_nbs)
        _result = []
        for i in result:
            if not self.check_num(self.graph.sent[i],line):
                continue
            _result.append(self.graph.sent[i])
        return _result,res

    def query(self):
        df = pd.DataFrame()
        df['map'] = ""
        df['kw'] = ""
        df['target'] = ""
        input_file = []
        cnt=0
        for _,_,docs in os.walk(TEST_PATH):
            for doc in docs:
                lines = open(os.path.join(TEST_PATH, doc)).readlines()
                #lines = pd.read_csv(os.path.join(TEST_PATH, doc)).iloc[:,1]
                lines = [lines[np.random.randint(len(lines))] for i in range(self.test_batch)]
                for line in lines:
                    line = utils.clr(line)
                    print(line)
                    result,res = self._query_one(line)
                    #result = self.addr_tree.words_route(res)
                    if len(result) == 0:
                        df.loc[str(cnt),'map'] = line
                        df.loc[str(cnt),'target'] = "".join([])
                        df.loc[str(cnt),'kw'] = ",".join(res)
                        cnt+=1
                        continue
                    else:
                        for parent_res in result:
                            print(line, parent_res)
                            df.loc[str(cnt),'map'] = line
                            df.loc[str(cnt),'target'] = "ROOT"+parent_res
                            df.loc[str(cnt),'kw'] = ",".join(res)
                            cnt+=1
                    df.to_csv("./record.csv")
                    print(cnt, 'save')

address_activity = Address_Acti()
def main():
    #ans = input("please input the address ")
    #print(address_activity.query_line(ans))
    address_activity.query()

if __name__ == "__main__":
    main()

