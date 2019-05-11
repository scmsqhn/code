#!/usr/bin/python
#coding:utf8

'''
Observer
'''
import sys
import pdb
import os
sys.path.append(os.environ['YUNYAN'])
sys.path.append(os.environ['ROOT'])
sys.path.append(os.environ['WORKBENCH'])
import pandas as pd
import myconfig
import multiprocessing
import init_data
from multiprocessing import Pool
import re
import activity_match
from activity_match import ActiMatch
import function_ultra
from function_ultra import utils
from function_ultra.mylog import logger as logger 
from reghelper import RegHelper
"""
核心思想是将所有地址序列标注后放入统一DataFrame中，使用碰撞融合纠错
"""

class StandAddrTreeBuilder(object):
    def __init__(self):
        self.df = pd.DataFrame(columns=myconfig.COLUMNS)
        self.thread_cnt = 10
        self.filename=myconfig.BAOTOU_STD_ADDRESS
        self.mRegHelper = RegHelper('dummy')
        logger.debug('实例化一个StandAddrTreeBuilder')

    def reg_filter(self,sentence):
        line = self.mRegHelper.address_formula(sentence)
        tuple_lst = re.findall("(.+?)/(.+?) ",line)
        return tuple_lst

    def data_generator(self):
        lines = open(self.filename,'r').readlines()
        #pool = Pool(processes=self.thread_cnt)  # 创建进程池
        #res = pool.map(self.reg_filter, [line for line in lines])
        for line in lines:
            res = self.reg_filter(line)
            yield res

    def insert_into_dataframe(self):
        logger.debug('数据插入dataframe开始')
        gen = self.data_generator() #生成数据
        for line in gen:
            res_dct={} #将输出定位dict
            logger.debug('数据插入dataframe开始 ' + str(line))
            for item in line:
               key = item[1]
               value = item[0]
               if not key in myconfig.COLUMNS: # 过滤掉序列标注错误
                   continue
               if key in res_dct:
                   res_dct[key]+="&"
                   res_dct[key]+=value
               else:
                   res_dct[key]=value
            ser=pd.Series(res_dct)
            df=pd.DataFrame(ser).T
            self.df=pd.concat([self.df,df], axis=0) # 将DataFrame按行拼接
            #print("self.df: ",self.df)
        self.df = self.df[myconfig.COLUMNS]
        self.df.to_csv(myconfig.dfpath,index=False)
        logger.debug('数据插入dataframe完毕')
        return myconfig.SUCCESS # 完成后返回结果

    # 这个方法明天要重新改写
    def format_tree(self,rootnode):
        # 数据对齐
        logger.debug('format_tree')
        node=rootnode
        for child in node.data:
            childnode = node.data.get(child)    
            if childnode:
                # 保证当一个层级只有两个名词时,nan+地址名词的时候,nan的stdchar也是
                if len(set(childnode.parent.data))==2 and ('nan' in "".join(list(set(childnode.parent.data)))):
                    for key in childnode.parent.data:
                        [nanin, nanout]=list(set(childnode.parent.data))
                        if 'nan' in childnode.parent.data.get(nanin).char:
                            stdchar = childnode.parent.data.get(nanout).char
                            childnode.parent.data.get(nanin).stdchar = stdchar
                            childnode.parent.data.get(nanout).stdchar = stdchar
                for key in childnode.parent.data:
                    brothernode = childnode.parent.data.get(key)
                    if childnode.char.split('/')[1] == brothernode.char.split('/')[1]:
                        ll = len((childnode.char.split('/')[0] and brothernode.char.split('/')[0]))
                        la = len(childnode.stdchar)
                        lb = len(brothernode.stdchar)
                        lmax = max(la,lb)
                        if len(re.findall("\d",childnode.char+brothernode.char))==0:
                            #如果两个部分有超过一半的汉字是重复的,且级别一致,就认为是一个级别的相同地址进行合并,stdchar合并
                            if ll/lmax > 0.5:
                                if la<=lb:
                                    childnode.stdchar=brothernode.stdchar
                                else:
                                    brothernode.stdchar=childnode.stdchar
            if childnode:
                self.format_tree(childnode)
        logger.debug('format_tree success')
        return myconfig.SUCCESS

    def transform_into_tree(self):
        # 将DataFrame输出为list生成器
        cols = self.df.columns
        for i in range(self.df.shape[0]):
            line = self.df.iloc[i,:]
            _line = ["%s/%s"%(m,n) for m,n in zip(line,cols)]
            yield _line

    def gen_std_tree(self):
        # 将df保存成一个树结构,保存后退出,返回SUCCESS
        gen=self.transform_into_tree()
        status=init_data.gen_std_tree_from_dataframe(gen, sav_file=myconfig.MY_TREE)
        logger.debug('从dataframe生成树并保存')
        #print('gen_std_tree ',status)
        return myconfig.SUCCESS

    def load_std_tree(self):
        # 从pkl读取树形结构
        std_tree=init_data.load_address_tree(sav_file=myconfig.MY_TREE)
        return std_tree

def test_data_2_tree():
    logger.debug('测试标准地址生成')
    mStandAddrTreeBuilder=StandAddrTreeBuilder() # 实例
    mStandAddrTreeBuilder.insert_into_dataframe() # 插入数据进入df
    mStandAddrTreeBuilder.gen_std_tree() # 生成树结构
    logger.debug('标准地址生成完毕')
    pdb.set_trace()
    
def test_search():
    logger.debug('搜索测试')
    acti_match_ins=ActiMatch('dummy') # 实例化用户管理实例
    res = acti_match_ins.search('包头市/CITY 青山区/DIST ') # 搜索
    logger.debug('搜索测试输出: %s'%res)  

def test_format_df():
    logger.debug('\n> 树的合并')
    from function_ultra import utils
    mStandAddrTreeBuilder=StandAddrTreeBuilder() # 实例
    my_tree=utils.read_var(myconfig.MY_TREE)
    mStandAddrTreeBuilder.format_tree(my_tree.root)
    utils.save_var(my_tree,myconfig.MY_TREE)
    pdb.set_trace()
    logger.debug('\n> 树的合并测试完成')

def show_tree():
    my_tree=utils.read_var(myconfig.MY_TREE)
    my_tree.show_tree(my_tree.root)
    pdb.set_trace()

if __name__=="__main__":
    test_data_2_tree()
    #test_data_2_tree()
    #test_format_df()
    #pdb.set_trace()
    #show_tree()
    pass

