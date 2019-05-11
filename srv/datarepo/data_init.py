#!encoding:utf-8
import subprocess
import json
import pdb
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
from redis import StrictRedis
import mylog
from mylog import logging 

logger = logging.getLogger() 
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler() 
consoleHandler.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler('log.log', mode='w', encoding='UTF-8') 
fileHandler.setLevel(logging.NOTSET)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
consoleHandler.setFormatter(formatter) 
fileHandler.setFormatter(formatter)

logger.addHandler(consoleHandler) 
logger.addHandler(fileHandler)
import myconfig 

STD_PATH = myconfig.STD_PATH
STD_FILE = myconfig.STD_FILE
TEST_PATH = myconfig.TEST_PATH
TEST_FILE = myconfig.TEST_FILE
SAVE_PATH = myconfig.SAVE_PATH
SAVE_FILE = myconfig.SAVE_FILE

FLAG_INIT_MODEL = False
FLAG_LOAD_MODEL = False

RE_NUMS = re.compile("\d+")

import sys
args = sys.argv[1:]
print(args)
if args[0] == "-i":
  if args[1] == "True":
    print("> INIT_MODEL")
    FLAG_INIT_MODEL = True
  else:
    FLAG_INIT_MODEL = False
if args[2] == "-l":
  if args[3] == "True":
    print("> LOAD_MODEL")
    FLAG_LOAD_MODEL = True
  else:
    FLAG_LOAD_MODEL = False

class Address_Acti(object):

    def __init__(self):
        self.batch = 10000
        self.test_batch = 100
        if FLAG_INIT_MODEL:
            print("init addr_tree")
            #self.addr_tree = Trie()
            print("init dict_tree")
            #self.dict_tree = Trie()
            print("init num_tree")
            #self.num_tree = Trie()
            print("init model")
            #self.init_model()
            print("init graph")
            #self.init_num_hash()
            self.graph = my_graph.My_Graph()
            logger.debug("init_model ok")
            pickle_helper.save(os.path.join(SAVE_PATH,SAVE_FILE),[self.addr_tree,self.dict_tree,self.graph,self.num_tree])
            logger.debug("pickle save ok")
        if FLAG_LOAD_MODEL:
            self.redis = StrictRedis(host='localhost', port=6379, db=0)
            #self.init_redis()
            self.addr_tree, self.dict_tree, self.graph = pickle_helper.load(os.path.join(SAVE_PATH,SAVE_FILE),[1,2,3])
            #self.addr_tree, self.dict_tree, self.graph = pickle_helper.load(os.path.join(SAVE_PATH,SAVE_FILE),[1,2,3])
            #self.addr_tree, self.dict_tree, self.graph,self.num_tree = pickle_helper.load(os.path.join(SAVE_PATH,SAVE_FILE),[1,2,3,4])
            self.nodes = set(self.graph.di.nodes())
            logger.debug("> pickle load ok ===")

    def init_redis(self):
      cmd = "cat redis_cmd_insert_data.txt | redis-cli --pipe"
      result = subprocess.getoutput(cmd)
      print(result)

    def _init_redis(self):
      stand_lines = open(os.path.join(STD_PATH, STD_FILE)).readlines()
      #stand_lines = pd.read_csv(os.path.join(STD_PATH, STD_FILE)).iloc[:,1]
      cnt = 0
      for line in stand_lines[:100000]:
        #logger.debug("redis init", line)
        #line = utils.clr(line)
        #words = list(jieba.cut(line))
        words = line.split(" ")
        for word in words:
          utils.add_sent_2_word(self.redis,word,str(hash(line)))
        cnt+=1
        if cnt%1000 == 1:
          print(cnt)
      return 0

    def cut_filter(self,src_sent):
        cmdin = r"区.+?与.+?交叉口[向东]?[\d+米]?路?[东南西北]?"

    def init_num_hash(self):
        stand_lines = pd.read_csv(os.path.join(STD_PATH, STD_FILE)).iloc[:,1]
        for line in stand_lines:
            """ insert address into addr_tree """
            """ insert all addr_tree """
            line = utils.clr(line)
            nums = list(re.findall(RE_NUMS,line))
            #self.num_tree.insert_num_lst(nums,hash(line))

    def init_model(self):
        #stand_lines = pd.read_csv(os.path.join(STD_PATH, STD_FILE)).iloc[:,1]
        stand_lines = open(os.path.join(STD_PATH, STD_FILE)).readlines()
        cnt = 0
        for line in stand_lines[:100000]:
            cnt += 1
            if cnt%10000==1:
                print(cnt)
            """ insert address into addr_tree """
            """ insert all addr_tree """
            #line = utils.clr(line)
            #words = list(jieba.cut(line))
            #nums = list(re.findall(RE_NUMS,line))
            #self.num_tree.insert_num_lst(nums,hash(line))
            #self.addr_tree.insert_wd_lst(words)
            words = line.split(" ")
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
            #logger.debug(i,j)
            if i == j:
                cnt+=1
                continue
            break
        if cnt == lmin and cnt>0:
            logger.debug(nums1 , " equal " ,nums2)
            return (cnt/lmin)*100
        elif cnt>0:
            logger.debug(nums1 , " equal " ,nums2)
            return (cnt/lmin)*100
        else:
            logger.debug(nums1, " not equal ", nums2)
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
            logger.debug(i,j)
            if i == j:
                cnt+=1
                continue
            break
        if cnt == lmin and cnt>0:
            logger.debug(nums1 , " equal " ,nums2)
            return True
        elif cnt>1:
            logger.debug(nums1 , " equal " ,nums2)
            return True
        else:
            logger.debug(nums1, " not equal ", nums2)
            return False

    def check_num(self, line1, line2):
        """ use num to check weather same or not """
        logger.debug("判断数字是否一致", line1,line2)
        cont = re.split("\d+",line1)[0]
        base = ""
        if len(cont)>0:
            #base = list(jieba.cut(cont))[-1]
            base = cont[-3:]
        nums1 = re.findall(RE_NUMS,line1)
        nums2 = re.findall(RE_NUMS,line2)
        logger.debug(line1, line2)
        logger.debug(nums1, nums2)
        lmin = min(len(nums1),len(nums2))
        #lmax = max(len(nums1),len(nums2))
        cnt = 0
        for i,j in zip(nums1[:lmin], nums2[:lmin]):
            logger.debug(i,j)
            if i == j:
                cnt+=1
                continue
            break
        if lmin>0:
            if not base+nums1[0] in line2:
                logger.debug("False",line1, line2)
                return False
        if cnt == lmin and cnt>0:
            return True
        elif cnt>0:
            return True
        else:
            logger.debug("False",line1, line2)
            return False

    def _check_num(self, line1, line2):
        """ use num to check weather same or not """
        base = ""
        cont = re.split("\d+",line1)[0]
        if len(cont)>0:
            #base = list(jieba.cut(cont))[-1]
            base = cont[-3:]
        nums1 = re.findall(RE_NUMS,line1)
        nums2 = re.findall(RE_NUMS,line2)
        logger.debug(line1, line2)
        logger.debug(nums1, nums2)
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
                logger.debug("False",base+nums1[0])
                return False
        if cnt == lmin and cnt>0:
            return True
        elif cnt>1:
            return True
        else:
            logger.debug("False",nums1, nums2)
            return False
    
    def _check(self,line1,line2):
        txts = re.split(RE_NUMS,line)
        if len(txts[0]) < 2:
            return False
        nums = re.findall(RE_NUMS,line)
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
            logger.debug(baseline , " is in ", line2)
            return True
        else:
            logger.debug(baseline , " not in ", line2)
            return False

    def common_nbs(self,comm_nbs):
        result = set()
        if len(comm_nbs)>1:
            result  = set(comm_nbs[0])
            for i in comm_nbs[1:]:
                if len(result & set(i))>0:
                    logger.debug("交集", len(result), len(set(i)))
                    result = result & set(i)
                    logger.debug(self.graph.sent[list(result)[0]])
                else:
                    return result
        elif len(comm_nbs)==1:
            result = comm_nbs[0]
        if len(result)>0:
            logger.debug("最终输出过滤后的标准地址", self.graph.sent[list(result)[0]])
        return result

    def check(self,line1,line2):
        txts = re.split(RE_NUMS, line)
        if len(txts[0]) < 2:
            return False
        nums = re.findall(RE_NUMS,line)
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
        logger.debug(baseline , " weather in ", line2)
        if len(re.findall(baseline,line2))>0:
            logger.debug(baseline , " bingo in ", line2)
            logger.debug(re.findall(baseline,line2))
            return True
        else:
            return False
        return False
    
    def word_filter(self, line_pre):
        res = []
        for word in line_pre.split(" "):
            #if self.dict_tree.search(word):
            #    res.append(word)
            res.append(word)
        return res
    
    def _query_one(self, line):
        """
        入口接口
        line 待比对内容,为一行文本
        地址可以看作三个部分
        文本部分 数字部分 和 量纲部分
        """
        line = utils.clr(line)
        output,res,score = [],[],[]
        #min_edit_value = 9999 #最小编辑距离
        my_txt = utils.without_num(line)#取出第一个数字前的文本部分
        my_num = re.findall(RE_NUMS,line)#取出数字部分
        result = self.route_text(my_txt,my_num)#根据文本部分和数字部分完成索引
        return result

    def prehand_one(self,line):
        """
        入口接口
        line 待比对内容,为一行文本
        地址可以看作三个部分
        文本部分 数字部分 和 量纲部分
        """
        line = utils.clr(line)
        output,res,score = [],[],[]
        #min_edit_value = 9999 #最小编辑距离
        my_txt = utils.without_num(line)#取出第一个数字前的文本部分
        my_num = re.findall(RE_NUMS,line)#取出数字部分
        result = self.pre_route_text(my_txt)#根据文本部分和数字部分完成索引
        one_piece = "%s&%s&%s&%s"%(line,my_txt,",".join(my_num),result)
        return one_piece

    def editDist(self, line, result):
        """get the minist edit distance of line with result"""
        min_edit_value = -1
        minist_one = ""
        for hs in list(result):
            try:
              standard_addr = self.graph.sent[hs]
            except:
              continue
            v = utils.compare_num(line, standard_addr)
            #v = utils.minEditDist(utils.get_nums(line), utils.get_nums(standard_addr))
            if v > min_edit_value:
                minist_one = hs
                min_edit_value = v
        #pdb.set_trace()
        return minist_one

    def _route_text(self,line,lst):
        """key algor the search algor"""
        line = utils.clr(str(line))
        """filter left the text word"""
        """how to filter use the dict-tree"""
        res = self.word_filter(line)
        words_route = []
        if " " in res:
           res.remove(" ")
        key_word_dict = {}
        for word in res:
          #pdb.set_trace()
          key_word_dict[word] = self.graph.di.degree()[word]
        sorted_key_word_dict = sorted(key_word_dict.items(),key=lambda d:d[1],reverse=False)
        key_word_lst = [word[0] for word in sorted_key_word_dict]
        neighbor = []
        for cursor in range(len(key_word_lst)):
          p_wd = key_word_lst[cursor]
          """get the common neighbors one by one when there is a word has no neighbors, continue"""
          """if there is a set of common_neighbor, & the set with last one"""
          print(p_wd,time.time())
          tmp_neighbor = utils.get_sent_from_word(self.redis, p_wd)
          if len(neighbor) == 0:
            neighbor.append(tmp_neighbor)
          if len(tmp_neighbor) > 0:
            if len(neighbor) > 0:
              tmp = neighbor[-1] & tmp_neighbor
              if len(neighbor[-1]) == len(tmp):
                print("查询到高级词召回数量没有变化",len(tmp))
                break
              if len(tmp) > 0:
                print("查询到高级词召回数量没有变化",len(tmp))
                break
              if len(tmp) == 0:
                continue
              else:
                neighbor[-1] = tmp
          else:
            continue
        if len(neighbor) == 0:
          """there is no neighor here"""
          return []
        else:
          return list(neighbor[-1])

    def pre_route_text(self,line):
        """key algor the search algor"""
        line = utils.clr(str(line))
        """filter left the text word"""
        """how to filter use the dict-tree"""
        res = self.word_filter(line)
        key_word_dict = {}
        logger.debug("过滤后词组" + ",".join(res))
        for word in res:
          if not word in self.nodes:
            continue
          key_word_dict[word] = self.degree[word]
        sorted_key_word_dict = sorted(key_word_dict.items(),key=lambda d:d[1],reverse=False)
        key_word_lst = [word[0] for word in sorted_key_word_dict]
        key_word_lst_sorted = ",".join(key_word_lst)
        return key_word_lst_sorted

    def route_text(self,line,lst):
        """key algor the search algor"""
        line = utils.clr(str(line))
        """filter left the text word"""
        """how to filter use the dict-tree"""
        res = self.word_filter(line)
        key_word_dict = {}
        logger.debug("过滤后词组" + ",".join(res))
        for word in res:
          key_word_dict[word] = self.graph.di.degree()[word]
        sorted_key_word_dict = sorted(key_word_dict.items(),key=lambda d:d[1],reverse=False)
        key_word_lst = [word[0] for word in sorted_key_word_dict]
        with open("key_word_lst.txt","a+") as g:
            g.write(",".join(key_word_lst)+"\n")
        return set()
        words_route = []
        neighbor = []
        logger.debug("排序后词组" + ",".join(key_word_lst))
        for cursor in range(len(key_word_lst)):
          p_wd = key_word_lst[cursor]
          neighbor.append(p_wd)
          if len(neighbor)>1:
            tmp_neighbor = utils.get_common_neighbor(self.redis, neighbor[-2], neighbor[-1])
            if len(tmp_neighbor)==0:
              continue
            else:
              words_route.append(tmp_neighbor)
              return words_route[-1]
              """
              if len(words_route)>0:
                tmp = tmp_neighbor & words_route[-1]
                if len(tmp)>0:
                  words_route[-1] = tmp
                else:
                  continue
              else:
                words_route.append(tmp_neighbor)
              """
        return words_route[-1] if len(words_route)>0 else set()
              
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
        f.flush()

    def save_one_txt(self,result,res,score,line,f):
        if len(result) == 0:
            f.write("%s,%s\n"%(line, "None"))
            f.flush()
            return 
        for parent_res in result:
            f.write("%s,%s\n"%(line, "ROOT"+self.graph.sent[parent_res]))
        f.flush()

    def filter(self,filter_name,line,output):
        if output == []:
          return ["None"]
        if filter_name == "edit_dis":
          target = self.editDist(line, output)
          return [self.graph.sent[target]]
        elif filter_name == "num_filter":
          num_lst = re.findall(RE_NUMS,line)
          if len(num_lst)>0:
            for num in num_lst:
              num_set = utils.get_sent_from_word(self.redis,num)
              if len(num_set) == 0:
                #return [self.graph.sent[target] for target in output]
                return output
              else:
                tmp = output & num_set
                if len(tmp) == 0:
                  return output
                else:
                  output = tmp
          return output 
                
def main(filename, lines):
    """
    filename 输出文件
    lines 待比对内容
    """
    with open(filename,"w+") as f:
      for line in lines:
        #logger.debug(line)
        output = address_activity.prehand_one(line)
        f.write(re.sub("\n","",output)+"\n")
        f.flush()

def sav_json(model):
    with open("./degree.json",'w',encoding='utf-8') as json_file:
        json.dump(model,json_file,ensure_ascii=False)
  
def load_json():
    model = {}
    with open("./degree.json",'r',encoding='utf-8') as json_file:
        model=json.load(json_file)
        return model

if __name__ == "__main__":
    address_activity = Address_Acti()
    sav_json(address_activity.graph.di.degree())
    address_activity.degree = load_json()
    filename = './output/doc_pre_handle.txt'
    lines = open(os.path.join(TEST_PATH,TEST_FILE)).readlines()
    lines = lines[1:]
    main(filename, lines)

