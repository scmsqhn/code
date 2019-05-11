# coding:utf-8
import sys
sys.path.append('..')
import business_ultra
import os
sys.path.append(os.environ['YUNYAN'])
sys.path.append(os.environ['ROOT'])
import myconfig
import myjieba_posseg as jieba
import os
import pdb
import re
import pandas as pd
import time
import numpy as np
import function_ultra
from function_ultra import utils
from function_ultra.mylog import logger

#import my_graph

STD_PATH = "/data/network/data/std/zz"
STD_FILE = "dz_zzxx_cs.csv"
TEST_PATH = "/data/network/data/test/zz"

class TrieNode(object):
    def __init__(self,char,node):
        self.data = {} # childs
        self.parent = node # parent
        self.char = char # char 北京市/市 
        self.stdchar = char # char 北京市/市 
        self.is_word = False
        self._id = np.random.randint(1000000)
        self.wealth = 1
        self.hash_set = set()
        self.lat=-1.0 
        self.lon=-1.0

    def show(self):
        logger.debug(self.__dict__)

class Trie(object):
    def __init__(self):
        self.root = TrieNode("ROOT",None)
        self.cursor = []

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

    def part_insert(self,rootnode,word):
        node=rootnode
        if not len(word)>0:
            node.is_word=True
            return myconfig.SUCCESS
        letter = word[0]
        kv=letter.split('/')
        key=kv[0]
        value=kv[1]
        letters=key.split('&')
        for letter in letters:
            _letter_="%s/%s"%(letter,value)
            child = node.data.get(_letter_)
            if not child:
                node.data[_letter_] = TrieNode(_letter_,node)
            else:
                node.data[_letter_].wealth += 1
            self.part_insert(node.data[_letter_],word[1:])

    def search(self, rootnode, word):
        node = rootnode
        for letter in word:
            node = node.data.get(letter)
            if not node:
                return False
        return node.is_word # 判断单词是否是完整的存在在trie树中

    def word_match(self,sent,result,lth=7):
        '''
        match address with one sentence
        '''
        print('\n> 标准词过滤',sent)
        lth = len(sent)
        i0 = 0
        for i in range(lth):
            if i < i0:
                continue
            for j in range(i,lth):
                if i>=j:
                    continue
                if self.search(self.root,sent[i:j]):
                    result.append(sent[i:j])
                    i0 = j
        print('\n> 标准词过滤',result)
        return result

    def get_all_parent_tree(self,nodes):
        parstrs = []
        if nodes:
            for node in nodes:
                parstr = []
                self.parent_tree(node,parstr)
                parstr = ' '.join(parstr[::-1])
                parstrs.append(parstr)
        return parstrs

    def scan_child_word(self,node,result):
        if len(result)>100:
            return 
        if node.is_word:
            result.append(node)
            print(result, 'append', node)
        for letter in node.data:
            if node.data.get(letter):
                childnode = node.data.get(letter)
                self.scan_child_word(childnode,result)
        #print('\nscan_child_word: ',result)

    def scan_node(self,rootnode,letter,result,n=3):
        '''
        遍历全树节点,深度n个高度
        '''
        n-=1
        if n<0:
            return result
        node = rootnode
        for child in node.data:
            if child == letter:
                #print('child',child)
                result.append(node.data.get(child))
                result = self.scan_node(node.data.get(child),letter,result,n)
        return result

    def scan_nodes(self,nodes,word,result):
        '''
        遍历全树,模糊查询查找某个词,逐级查找，一直到找不到节点为止
        '''
        if word == []:# or nodes == []:
            return result
        for letter in word:
            __result = []
            for node in nodes:
                __result = self.scan_node(node,letter,__result)
                #print(self.get_all_parent_tree(__result))
                #print('__result',__result)
                #pdb.set_trace()
            if __result == []:
                word = word[1:]
                result = self.scan_nodes(nodes,word,result)
            else:
                word = word[1:]
                result = __result
                result = self.scan_nodes(__result,word,result)
        result = list(set(result))
        #print('_result_',result)
        return result

    def isParent(self,child,parent):
        if child.char == 'ROOT':
            return False
        if child.parent == parent:
            return True
        else:
            return self.isParent(child.parent,child.parent.parent)

    def parent_tree(self,node,parstr):
        #print(node.parent.char)
        #pdb.set_trace()
        try:
            if node.char == "ROOT":
                return 
            if node.parent.char == "ROOT":
                #print(parstr[::-1])
                parstr.append(node.stdchar)
                #print('\n> prent_tree ',"".join(parstr[::-1]))
                return parstr
            else:
                parstr.append(node.stdchar)
                parstr = self.parent_tree(node.parent, parstr)
        except:
            pdb.set_trace()

    def show_tree(self,rootnode):
        node=rootnode
        for child in node.data:
            childnode = node.data.get(child)
            if not childnode:
                continue
            childnode.show()
            pdb.set_trace()
            self.show_tree(childnode)

    def trans_tree_2_graph(self,rootnode,graph):
      try:
        node = rootnode
        for child in node.data:
            print(node.__dict__)
            childnode = node.data.get(child)

            if not childnode:
                print('childnode None')
                continue
            elif 'nan' in childnode.char:
                print('childnode nan')
                continue
            else:
                print('go ahead')
                pass

            childnode_char=childnode.char
            node_char=node.char

            if graph.get_edge_data(node_char,childnode_char):
                _wealth = graph.get_edge_data(node_char,childnode_char)['wealth']
                _wealth+=childnode.wealth
                graph.get_edge_data(node_char,childnode_char)['wealth']=_wealth
                print(graph.get_edge_data(node_char,childnode_char)['wealth'])
            else:
                graph.add_edge(node_char,childnode_char,wealth=childnode.wealth)
            self.trans_tree_2_graph(childnode,graph)
      except:
        import traceback
        traceback.print_exc()
        pdb.set_trace()

if __name__ == '__main__':
    import business_ultra
    from business_ultra import init_data
    from business_ultra import activity_match
    #business_ultra.init_data.gen_std_tree_from_dataframe()
    my_tree = utils.read_var(myconfig.MY_TREE)
    pdb.set_trace()
    my_tree.show_tree(my_tree.root)

    acti_match_ins = activity_match.ActiMatch('dummy')
    #gen = acti_match_ins.read_file(myconfig.STDTXTPATH)
    lst = []
    lst.append(['青山区/DIST'])
    def gen():
        for i in lst:
            yield i 

    gen = gen()
    while(1):
        item = gen.__next__()
        res = acti_match_ins.search(item)
        print(item ,res)
        print('\n>结果:%s\n输入:%s'%(res,item))


