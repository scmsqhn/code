#!

import os
import sys
os.environ['ROOT']='/data'
#os.environ['YUNYAN']='/root/yunyan'
#os.environ['WORKBENCH']='/root'
os.environ['YUNYAN']='/root/yunyan/'
os.environ['WORKBENCH']='/data'
sys.path.append(os.environ['ROOT'])
sys.path.append(os.environ['YUNYAN'])
sys.path.append(os.environ['WORKBENCH'])
sys.path.extend(['.','..','../..','./business_ultra'])
print(sys.path)
import pdb
#pdb.set_trace()
import re
import time
import business_ultra
print(__file__)

INIT_READY=False
INIT_SEARCH_READY=False
INIT_MATCH_READY=False
#pathconfigure
print(os.environ['YUNYAN'])
print(os.environ['ROOT'])
PRJPATH=os.environ['YUNYAN']
pth=lambda x:os.path.join(PRJPATH,x)
cur=lambda:os.path.dirname(os.path.realpath(__file__))
CURPATH=cur()
MODPATH=pth('model')
dfpath=pth('data/dfpath.csv')
SRCPATH=pth('src')
DATPATH=pth('data')
STDADD=pth('data/standard_addr.json')
CLASSMODPATH=pth('model/classifier.model')
CLASSMODPATH2=pth('model/classifier.model')
DCTPATH=pth('dct_file/dct_level')
DICT=pth('data/dict.txt')
PREPATH=pth('dct_file/dct_level/pre.txt')
STDPATH=pth('data/standard_addr.json')
DIGRAPH=pth('data/di_graph.pkl')
STDTXTPATH=pth('data/baotou_addr/std_addr_dict.txt')
#STDTXTPATH=pth('data/yyap.txt.bak')
ZHUJIANPATH=pth('data/zhujian.txt')
FEEDPATH=pth('data/yyap.txt')
#STDTXTPATH=pth('data/yyap.txt')
MY_TREE=pth('data/my_tree.pkl')
MY_WORD=pth('data/my_word.pkl')
INIT_READY=False
ADDR_TREE_READY=False
sys.path.append(SRCPATH)

#rightnow
rnow=lambda:time.time()
#asctime
asctime=lambda:time.asctime(time.localtime(time.time()))
#localtime
localtime=lambda:time.strftime("%Y-%m-%d%H:%M:%S",time.localtime())

#configure
CHAR_HASH_DIVIDE=3000
LENTH_PADDING=15
TRAIN_DATA=10
EVAL_DATA=3
HASH_MAX=77777777

#regconfigure
CHECK_RULE_JIEDAO=re.compile("\D\D\D[街道路巷村镇坡屯]")
CHECK_RULE_LOUHAO=re.compile("([一二三四五六七八九零]+?[号杠])(?:.*?)?([一二三四五六七八九零]+?[号杠$])")


#=
zhengzhou_std_word=pth('model/zhengzhou_std_word.pkl')
zhengzhou_std_tree=pth('model/zhengzhou_std_tree.pkl')
#=
ZZ_STD_ADD='/data/network_zz/data/test/zz/'
ZZ_STD_ADD_TREE=pth('model/zz_add_tree.pkl')
ZZ_STD_WORD_TREE=pth('model/zz_word_tree.pkl')

#redisconfigure
RDSHOST='localhost'
RDSPORT=6379

#mongodbconfigure
MDBHOST='127.0.0.1'
MDBPORT=27717

'''
>attachlist
deeplearningmodel
'''

#INIT_READY=False
ATTACH_LST={}
#from business_ultra.myHandlerimport DeepLearningViewer
#from business_ultra.myHandlerimport MachineLearnViewer
#from business_ultra.myHandlerimport RegRuleViewer

#ATTACH_LST['dl']=DeepLearningViewer
#ATTACH_LST['ml']=MachineLearnViewer
ATTACH_LST=[]
ATTACH_LST.append('AddrMatch')
ATTACH_LST.append('RegRuleViewer')

'''
redissetting
'''
REDIS_HOST_DAT='localhost'
REDIS_HOST_DAT_PORT=6379

SPLIT_RES='1'
SEARCH_RES='2'
MATCH_RES='3'
PRED_RES='5'
POSSEG_CUT_RES='6'
COLUMNS_DCT={'省':'PROV','市':'CITY','区':'DIST','社区':'SHEQU','村居委会':'CJWH',\
'自然村组':'ZRCZ','街路巷名':'JLX','门牌号':'MPH','小区名':'XIAOQU','组团名称':'ZUTUAN',\
'建筑物名称':'JZW','栋号':'DONGHAO','单元号':'DYH','楼层':'LOUC','户室号':'HSH'}
COLUMNS=['PROV','CITY','DIST','SHEQU','CJWH','ZRCZ','JLX','MPH','XIAOQU','ZUTUAN','JZW','DONGHAO','DYH','LOUC','HSH']
BAOTOU_STD_ADDRESS=pth('data/baotou_std_addr_base.txt')

SUCCESS = 'success'
FAILURE = 'failure'




