# coding:utf-8
import sys
import os
sys.path.append(os.environ['YUNYAN'])
sys.path.append(os.environ['ROOT'])
import myjieba as jieba
import os
import pdb
import re
import pandas as pd
import time
import numpy as np
#import my_graph

STD_PATH = "/data/network/data/std/zz"
STD_FILE = "dz_zzxx_cs.csv"
TEST_PATH = "/data/network/data/test/zz"

class TrieNode(object):
    def __init__(self,char,node,level):
        self.data = {} # childs
        self.parent = node # parent
        self.char = char # char 北京市/市 
        self.is_word = False
        self._id = ''
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

    def insert_id_word(self,sent):
        node = self.root
        _id, word = sent.split(',')
        for letter in word:
            child = node.data.get(letter)
            if not child:
                node.data[letter] = TrieNode(letter,node)
            else:
                node.data[letter].wealth += 1
            node = node.data[letter]
        node.is_word = True
        node._id = _id

    def fuzzy_insert(self,word):
        if len(word)<1:
            return
        result = []
        result = self.scan_node(self.root,word[0],result)
        node = self.root
        for letter in word:
            child = node.data.get(letter)
            if not child:
                node.data[letter] = TrieNode(letter,node)
            else:
                node.data[letter].wealth += 1
            node = node.data[letter]
        node.is_word = True

    def insert_node(self, node, word):
        for letter in word:
            child = node.data.get(letter)
            if not child:
                node.data[letter] = TrieNode(letter,node)
            else:
                node.data[letter].wealth += 1
            node = node.data[letter]
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

    def search_words(self, rootnodes):
        result = []
        for rootnode in rootnodes:
            result = self.search_word(rootnode, result)
        return result

    def search_word(self, rootnode, result):
        node = rootnode
        for letter in node.data:
            child = node.data.get(letter)
            if child:
                if child.is_word == True:
                    result.append(child)
                result = self.search_word(child, result)
        return result

    def __search__(self, rootnode, word):
        node = rootnode
        for letter in word:
            node = node.data.get(letter)
            if not node:
                return False
        return node.is_word,node._id # 判断单词是否是完整的存在在trie树中

    def fuzzy_search(self, rootnode, word):
        node = rootnode
        for letter in word:
            node = node.data.get(letter)
            if not node:
                return word.index(letter)
        return node.is_word # 判断单词是否是完整的存在在trie树中

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

    def search_node(self,rootnode,letter):
        '''
        seem like search ,but only search word
        '''
        node = rootnode
        if not node.data.get(letter):
            return False
        return node.data.get(letter)

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
        if not type(node) == Trie:
            return result
        if node.is_word == True:
            result.append(node)
            return result
        for letter in node.data:
            node = node.data.get(letter)
            if node:
                self.scan_child_word(node,result)
        return result

    def scan_word(self,word):
        '''
        遍历全树，没找到合适节点
        '''
        node = self.root
        for letter in word:
            child = node.data.get(letter)
            if not child:
                node = child
                word = word[1:]
                continue

    def scan_nodes(self,rootnode,word,result):
        """ get all the word in tree return nodes"""
        node = rootnode
        if len(word) == 0:
            return result
        node = rootnode.data.get(word[0])
        if node:
            result.append(node)
            result = self.scan_nodes(node,word[1:],result)
        else:
            for letter in rootnode.data:
                node = rootnode.data.get(letter)
                if node:
                    result = self.scan_nodes(node,word,result)
        return result

    def scan_child_word_from_nodes(self,nodes,result):
        for node in nodes:
            result = self.scan_child_word(node,result)
        return result

    def __get_all_parent_tree__(self,nodes):
        parstrs = []
        _ids = []
        for node in nodes:
            _ids.append(node._id)
            parstr = []
            self.parent_tree(node,parstr)
            parstr = ''.join(parstr[::-1])
            parstrs.append(parstr)
        return parstrs,_ids

    def get_all_parent_tree(self,nodes):
        parstrs = []
        for node in nodes:
            parstr = []
            self.parent_tree(node,parstr)
            parstr = ''.join(parstr[::-1])
            parstrs.append(parstr)
        return parstrs

    def node_seem_scan(self,targetnode,root,level=2):
        '''
        get all letter in the tree from one node
        '''
        node = root
        result = True
        seem_like_nodes = []
        for child in node.data:
            result = self.node_seem(targetnode,node.data.get(child),result,level)
            if result:
                seem_like_nodes.append(node.data.get(child))
        return seem_like_nodes

    def node_seem(self,node,bronode,result,n):
        if node.data == {}:
            if bronode.data == {}:
                return True
        if n>0:
            for childnode in node.data:
                pre = node.data.get(childnode,'')
                aft = bronode.data.get(childnode,'')
                if not pre == aft:
                    return False
                result = self.node_seem(pre,aft,result,n-1)
            for chidnode in bronode.data:
                pre = node.data.get(childnode,'')
                aft = bronode.data.get(childnode,'')
                if not pre == aft:
                    return False
                result = self.node_seem(pre,aft,result,n-1)
        return True


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
        if node.parent.char == "ROOT":
            #print(parstr[::-1])
            parstr.append(node.char)
            #print('\n> prent_tree ',"".join(parstr[::-1]))
            return parstr
        else:
            parstr.append(node.char)
            parstr = self.parent_tree(node.parent, parstr)

    def starts_with(self, prefix):
        node = self.root
        for letter in prefix:
            node = node.data.get(letter)
            if not node:
                return False
        return True

    def fuzzy_search_address(self, node, word):
        if len(word)<1:
            return node
        result = []
        result = self.scan_node(self.ROOT, word[0], result)
        for node in result:
            if self.fuzzy_search(node.parent, word) == True:
                return node

    def words_route(self,words):
        nodes = [self.root]
        result = []
        result = self.scan_word(nodes,words)
        #print(result)
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

def node_join(node1, node2):
    assert node1.char == node2.char
    for letter in node2.data:
        node1.data[letter] = node2.data.get(letter)
    node1.parent.extend(node2.parent)
    if node2.is_word == True:
        node1.is_word = False
    node1.wealth+=node2.wealth
    for i in node2.hash_set:
        node1.add(i)
    return node1

def node_merge(node ,childTree):
    '''
    合并两颗树,将子树合入父树
    '''
    for letter in node.data:
        node = node.data.get(letter)
        if similar(node,childTree):
            node = node_join(node,childTree)
            return node # merge succ
        for letter in node.data:
            node = node.data.get(letter)
            node_merge(node ,childTree)
    return node

def merge_self(tree_parent):
    result = []
    node = tree_parent.root
    for letter in node.data:
        data = node.data.get(letter)
        tree_parent.scan_node(data,letter,result)

def merge_tree(tree_parent, tree_child):
    for letter in tree_parent.data:
        node = tree_parent.get(letter)
        node = node_merge(node ,list(tree_child.data)[0])
        tree_parent[letter] = node
    return tree_parent

def similar(node,childTree):
    '''
    if the is similar
    '''
    '''
    读入数据，通过树结进行合并融合
    '''
    pass
    '''

    weight = [0.6,0.3,0.1]
    score = []
    if childTree.char == node.char:
        score.append(1.0)
    sec_level_2,sec_level_2 = []
    for char in node.data:


        for letter in node.data:
            if letter in childTree.data:
                return True
    return False
    '''

if __name__ == '__main__':
    pass
