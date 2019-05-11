#!coding=utf-8

import sys
import os
sys.path.append(os.environ['YUNYAN'])
sys.path.append(os.environ['WORKBENCH'])
import myconfig
import os
import function_ultra.utils as utils
#import function_ultra.utils_back_trans as utils_back_trans
import pdb
import myjieba_posseg as jieba
#import xgboost as xgb
import re
import pdb
import json
import numpy as np
import threading
from time import ctime,sleep
import sys
import business_ultra.mark_train_data as mark_train_data
import time
#import xgboost as xgb
import myconfig
def load_model(model_name):
    bst_new = xgb.Booster()
    bst_new.load_model(model_name)
    return bst_new
global BST
CURPATH = os.path.dirname(os.path.realpath(__file__))


def init_jieba():
    pf = os.walk(myconfig.DCTPATH)
    jieba.load_userdict(myconfig.PREPATH)
    for path,_,files in pf:
      for filename in files:
        if filename == 'tokens.txt':
            continue
        if not filename.split('.')[-1] == 'txt':
            continue
        f = os.path.join(path,filename)
        jieba.load_userdict(f)
        print('load_userdict', f)

#jieba.load_userdict(myconfig.DICT)

standard_dct = {}
DEBUG = False
CURPATH = os.path.dirname(os.path.realpath(__file__))

''''''
sheng_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"省.txt")).readlines()])
shi_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"市.txt")).readlines()])
qu_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"区.txt")).readlines()])
shequ_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"社区.txt")).readlines()])
cunjuweihui_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"村居委会.txt")).readlines()])
jieluxiangming_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"街路巷名.txt")).readlines()])
zirancunzu_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"自然村组.txt")).readlines()])
menpaihao_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"门牌号.txt")).readlines()])
xiaoqu_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"小区名.txt")).readlines()])
zutuan_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"组团名称.txt")).readlines()])
''''''
donghao_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"栋号.txt")).readlines()])
danyuanhao_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"单元号.txt")).readlines()])
louceng_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"楼层.txt")).readlines()])
hushihao_ciku = set([re.sub("\n","",line.split(' ')[0]) for line in open(os.path.join(myconfig.DCTPATH,"户室号.txt")).readlines()])
''''''
dict_set_lst = [sheng_ciku,shi_ciku,qu_ciku,shequ_ciku,cunjuweihui_ciku,jieluxiangming_ciku,zirancunzu_ciku,menpaihao_ciku,xiaoqu_ciku,zutuan_ciku,donghao_ciku,danyuanhao_ciku,louceng_ciku,hushihao_ciku]
full_level_keys = ["省","市","区","社区","村居委会","街路巷名","自然村组","门牌号","小区名","组团名称","栋号","单元号","楼层","户室号"]
level_keys = ["省","市","区","社区","村居委会","街路巷名","自然村组","门牌号","小区名","组团名称","栋号","单元号","楼层","户室号"]
assert len(dict_set_lst) == len(full_level_keys)
stanard_keys = ['city', 'ld', 'room', 'floor', 'street', 'unit', 'doornum', 'group', 'community', 'committee', 'village', 'province', 'county', 'xiaoqu', 'juweihui', 'shequ']
global global_cnt
global_cnt = 0

'''
生成级别与词库键值对
'''
level_words_kv = {}
for level_key,words_set in zip(level_keys,dict_set_lst):
    level_words_kv[level_key] = words_set

def init_global_cnt():
    global_dct = {\
    '省': 0, \
    '市': 1, \
    '区': 2, \
    '社区': 3, \
    '村居委会': 4, \
    '自然村组': 5, \
    '街路巷名': 6,\
    '小区名': 7, \
    '门牌号': 8, \
    '组团名称': 9, \
    '建筑物名称': 10, \
    '楼层': 12, \
    '栋号': 13, \
    '单元号':14, \
    '户室号': 15, \
    '其他': 16, \
    }

    global_num_dct = {}
    for k in global_dct:
        global_num_dct[global_dct[k]] = k
    return global_dct, global_num_dct

def load_model(model_name):
    bst_new = xgb.Booster()
    bst_new.load_model(model_name)
    return bst_new

def init_classifier_model(model_name):
    return load_model(model_name)


global_dct, global_num_dct = init_global_cnt()

def get_ready_my_dict():
    with open(myconfig.STDPATH) as f:
        cont = f.read()
        standard_addr = json.loads(cont)
    standard_dct = {}
    ks = []
    vs = []
    for item in standard_addr['RECORDS']:
        v = item['name']
        k = item['type']
        ks.append(k)
        vs.append(v)

    keys = list(set(ks))
    values = list(set(vs))

    for k in keys:
        standard_dct[k] = []

    for item in standard_addr['RECORDS']:
        v = item['name']
        k = item['type']
        if not v in standard_dct[k]:
            standard_dct[k].append(v)
    standard_dct['xiaoqu']=[]
    standard_dct['juweihui']=[]
    standard_dct['shequ']=[]

    with open(os.path.join(myconfig.DCTPATH,'小区名.txt'),'r') as g:
        lines = g.readlines()
        for line in lines:
            standard_dct['xiaoqu'].append(re.sub("[\r\n]","",line))

    with open(os.path.join(myconfig.DCTPATH,'村居委会.txt'),'r') as g:
        lines = g.readlines()
        for line in lines:
            standard_dct['juweihui'].append(re.sub("[\r\n]","",line))

    with open(os.path.join(myconfig.DCTPATH,'社区.txt'),'r') as g:
        lines = g.readlines()
        for line in lines:
            standard_dct['shequ'].append(re.sub("[\r\n]","",line))
    return standard_dct

standard_dct = {}

dict_clus = {}
for k in level_keys:
    with open(os.path.join(myconfig.DCTPATH,"%s.txt"%k)) as f:
        lines = f.readlines()
        lines = [re.sub("[^\u4e00-\u9fa50-9a-zA-Z\-]","",line) for line in lines]
        dict_clus[k] = lines

stanard_keys = ['city', 'ld', 'room', 'floor', 'street', 'unit', 'doornum', 'group', 'community', 'committee', 'village', 'province', 'county', 'xiaoqu', 'juweihui', 'shequ']
str_xiaoqu = "|".join(standard_dct.get('xiaoqu',''))
str_xiaoqu = "(?:"+str_xiaoqu+")?"

sheng = re.compile('(.+省)?')
shi = re.compile('(.{2,3}(?<!区)市(?!巷))?')
qu = re.compile("\D&\d")
shequ = re.compile(r'([\u4e00-\u9fa5]+(?:乡|镇(?!委会)|办事处|社区服务中心|社区|片区))?$')
cunjuweihui = re.compile(r'([\u4e00-\u9fa5]+(?:委会|村委会|村委会|村民委员会|村委员会|居委会|创业园|(?<!新)村(?![街道路巷民组苑])))?(?:服务中心)?(?<!商铺)')
zirancunzu = re.compile(r'(.+(?:(?:组(?![团新])|村(?!民))))?$')
jieluxiang = re.compile(r'([\u4e00-\u9fa5]+(?:段|街|路|巷|道|家[湾弯]|坡(?=\d)|地块|[东南西北]侧)(?!组)$)?(?:空头户)?$')
menpaihao = re.compile(r'(散居\d+|(?:散居|新|附|门面|门面房)?[a-zA-Z\d一二三四壹贰叁肆五六七八九十\-]+号(?:地块)?(?!楼)(?:附\d+号(?!$))?|\d+网格|散居\d+(?=\d0)|\d+号)?')
xiaoqu = re.compile(r'(.+?小区|[\u4e00-\u9fa5\-]*?(?=[附a-zA-Z\d一二三四五六七八九十甲乙丙丁戊贰叁肆玖(?:老三|壹栋)?]+[(?:壹栋)幢栋单元号楼期区(?:网格)?])|龙城壹号|老三栋|.+?(?:家属|工业|生活)区|.+?(?:地质队)|.+?厂[东西南北一二三四]区|%s$)?$'%str_xiaoqu)
jianzhuwu = re.compile(r'(?<![一二三四壹贰叁肆五六七八九十甲乙丙丁戊])(?<![期栋])([a-zA-Z\d\u4e00-\u9fa5]+(?:宿舍|大厦|广场|综合体|健身中心))?')
zutuan = re.compile(r'(\d+网格|(?![\d甲乙丙丁一二三四壹贰叁肆五六七八九十壹]+栋)[^附]+(?:组团|区)(?:[a-zA-Z\d]+区)?(?:\d期)?|[东南西北壹贰叁伍拾\dA-Za-z一二三四壹贰叁肆五六七八九十]+区|甲乙丙丁戊|\d+期|\d+网格|[\d一二三四五]+区[\d一二三四五]+期|[一二三四五六七八九十壹贰叁肆]+(?:期|组团)$)?(?:保障房)?$')
louhao = re.compile(r'((?:附)?[\da-zA-Z]+(?:号楼)$|办公楼$|号(?=[\da-zA-Z一二三四五]+栋)$|\d+号(?!$)$)?$')
donghao = re.compile(r'((?:[\u4e00-\u9fa5]+?)?(?:经济适用房)?(?:商铺)?[\da-zA-Z至甲乙丙丁首一二三四壹贰叁肆五六七八九十东南西北壹贰叁肆伍\-]+?[栋幢座](?:[\u4e00-\u9fa5]+阁)?$)?$')
danyuan = re.compile(r'([\da-zA-Z一二三四壹贰叁肆五六七八九十甲乙丙丁]+单元$)?$')
louceng = re.compile(r'((?:[负附])?[\d一二三四壹贰叁肆五六七八九十a-zA-Z]+?[楼层]$|[一二三四壹贰叁肆五六七八九十]+层$)?$')
hushihao = re.compile(r'((?:[\da-zA-Z]+型)?正?(?:[\da-zA-Z]+)*?[负附付夹底夹底地下层]*?[门面\da-zA-Z\-、]+[号幢室]+?(?:附[\d+一二三四壹贰叁肆五六七八九十]+号)?|\d+室$|\d+号$|附?[\d一二三四壹贰叁肆五六七八九十]+号门面|[a-zA-Z]座|\d+0\d+$|\d+$)?(?:空挂户)?$')
reg_lst = [sheng,shi,qu,shequ,cunjuweihui,jieluxiang,zirancunzu,menpaihao,xiaoqu,zutuan,donghao,danyuan,louceng,hushihao]
level_keys = ["省","市","区","社区","村居委会","街路巷名","自然村组","门牌号","小区名","组团名称","栋号","单元号","楼层","户室号"]

assert len(reg_lst) == len(level_keys)

def __reg_level_match(word,lastlevel):
    if find(sheng,word) and not level_keys.index("省")<=level_keys.index(lastlevel):
            return "省"
    elif find(shi,word) and not level_keys.index("市")<=level_keys.index(lastlevel):
            return "市"
    elif find(qu,word) and not level_keys.index("区")<=level_keys.index(lastlevel):
            return "区"
    elif find(shequ,word) and not level_keys.index("社区")<=level_keys.index(lastlevel):
            return "社区"
    elif find(cunjuweihui,word) and not level_keys.index("村居委会")<=level_keys.index(lastlevel):
            return "村居委会"
    elif find(zirancunzu,word) and not level_keys.index("自然村组")<=level_keys.index(lastlevel):
            return "自然村组"
    elif find(jieluxiang,word) and not level_keys.index("街路巷名")<=level_keys.index(lastlevel):
            return "街路巷名"
    elif find(menpaihao,word) and not level_keys.index("门牌号")<=level_keys.index(lastlevel):
            return "门牌号"
    elif find(xiaoqu,word) and  not level_keys.index("小区名")<=level_keys.index(lastlevel):
            return "小区名"
    elif find(jianzhuwu,word) and not level_keys.index("建筑物名称")<=level_keys.index(lastlevel):
            return "建筑物名称"
    elif find(zutuan,word) and not level_keys.index("组团名称")<=level_keys.index(lastlevel):
            return "组团名称"
    elif find(donghao,word) and not level_keys.index("栋号")<=level_keys.index(lastlevel):
            return "栋号"
    elif find(danyuan,word) and not level_keys.index("单元号")<=level_keys.index(lastlevel):
            return "单元号"
    elif find(louceng,word) and not level_keys.index("楼层")<=level_keys.index(lastlevel):
            return "楼层"
    elif find(hushihao,word) and  not level_keys.index("户室号")<=level_keys.index(lastlevel):
        return "户室号"
    else:
        pass

def reg_level_match(word,lastlevel):
    '''
    通过正则找到对应的区间
    '''
    if find(sheng,word):
            return "省"
    elif find(shi,word):
            return "市"
    elif find(qu,word):
            return "区"
    elif find(shequ,word):
            return "社区"
    elif find(cunjuweihui,word):
            return "村居委会"
    elif find(zirancunzu,word):
            return "自然村组"
    elif find(jieluxiang,word):
            return "街路巷名"
    elif find(menpaihao,word):
            return "门牌号"
    elif find(xiaoqu,word):
            return "小区名"
    elif find(jianzhuwu,word):
            return "建筑物名称"
    elif find(zutuan,word):
            return "组团名称"
    elif find(donghao,word):
            return "栋号"
    elif find(danyuan,word):
            return "单元号"
    elif find(louceng,word):
            return "楼层"
    elif find(hushihao,word):
        return "户室号"
    else:
        idx = level_keys.index(lastlevel)+1
        if idx > 15:
            idx = 15
        return level_keys[idx]

def find(reg,word):
    if len(re.findall(reg,word)[0])>0:
        return True
    else:
        return False

def get_level(word, lastlevel):
    flag = ""
    for k in level_keys:
        if word in dict_clus[k]:
            return k
    flag = reg_level_match(word,lastlevel)
    return flag

def union_lst(cuts):
    res = []
    tmp = ""
    for cut in cuts:
        if len(re.findall("[\u4e00-\u9fa5]",cut))==0:
            tmp+=cut
        elif cut == "附":
            tmp+=cut
        else:
            tmp+=cut
            res.append(tmp)
            tmp = ""
    if len(tmp)>0:
        res.append(tmp)
        tmp = ""
    return res

def trans(chars):
    DIV = myconfig.CHAR_HASH_DIVIDE
    size = myconfig.LENTH_PADDING
    padding = []
    for char in chars:
        char_num = ord(str(char))
        char_num = char_num%DIV
        padding.append(char_num)
        pass
    if not len(padding)-size>=0:
        padding.extend([ord(" ")%DIV]*size)
    pass
    return padding[:size]

def dct_trans(k,global_dct):
    res = global_dct[k]
    return res

def get_word_level(k,v,bst):
    X_train,y_train = [],[]
    X_train.append(trans(v))
    y_train.append(dct_trans(k,global_dct))
    d_pred = xgb.DMatrix(np.array(X_train).reshape(-1,myconfig.LENTH_PADDING), label=np.array(y_train).reshape(-1))
    pred = bst.predict(d_pred)
    return global_num_dct[int(pred[0])]

def _get_words_level(cuts,bst):
    pass
    resdct = {}
    lastword = ""
    for word in cuts:
        level = get_word_level("省",lastword+word,bst)
        lastword = word
        if level in resdct:
            resdct[level] = resdct[level]+","+word
        else:
            resdct[level] = word
    return resdct

def isNotNull(dct):
    for k in dct:
        if not dct.get(k,'') == '':
            return True
    return False

def comb(dct1,dct2):
    print(dct2, dct1)
    dct = {}
    for k in dct1:
        assert not k in dct
        dct[k] = dct1[k]
    for k in dct2:
        if k in dct1:
            continue
        assert not k in dct
        dct[k] = dct2[k]
    return dct

def dict_search(words):
    level_keys = ["省","市","区","社区","村居委会","街路巷名","自然村组","门牌号","小区名","组团名称","栋号","单元号","楼层","户室号"]
    dct_5 = pick(level_keys,words)
    return dct_5

def _dict_search(words):
    '''
    解决门牌号乱序的问题
    '''
    level_keys = ["省","市","区","社区","村居委会","街路巷名","自然村组","门牌号","小区名","组团名称","栋号","单元号","楼层","户室号"]
    print(level_keys[8:10])
    dct_1 = pick(['小区名'], words)
    dct_10 = pick(['组团名称'], words)
    if isNotNull(dct_1):
        idy = words.index(list(dct_1.values())[0])
        dct_2 = pick(level_keys[:8],words[:idy])
        print(':',words[:idy])
        dct_3 = pick(level_keys[8:],words[idy:])
        print('::',words[idy:])
        dct_4 = comb(dct_2,dct_3)
        print('>dct_2',dct_2)
        print('>dct_3',dct_3)
        print('0 dct_4',dct_4)
        return dct_4
    elif isNotNull(dct_10):
        idy = words.index(list(dct_10.values())[0])
        dct_2 = pick(level_keys[:9],words[:idy])
        dct_3 = pick(level_keys[9:],words[idy:])
        dct_4 = comb(dct_2,dct_3)
        print('>>dct_2',dct_2)
        print('>>dct_3',dct_3)
        print('1 dct_4',dct_4)
        return dct_4
    else:
        level_keys = ["省","市","区","社区","村居委会","街路巷名","自然村组","门牌号","栋号","单元号","楼层","户室号"]
        dct_5 = pick(level_keys,words)
        print('2 dct_5',dct_5)
        return dct_5

def pick(level_keys,words):
    js_dct = jsdct(level_keys,words)
    if js_dct == {}:
        return {}
    return ret(words,js_dct,level_keys)

def jsdct(lst,words):
    js_dct = {}
    for level_key,words_set in zip(full_level_keys,dict_set_lst):
        if not level_key in lst:
            continue
        for word in words:
           if word in words_set:
               js_dct['%s_%s'%(level_key,word)] = 1
    return js_dct

def ret(words,js_dct,lst):
    level_keys = []
    for i in full_level_keys:
        if i in lst:
            level_keys.append(i)
    result = {}
    ret = mark_train_data.addr_classifier(level_keys,words,js_dct,0)
    for i,j in zip(ret[3],ret[4]):
        k,v = level_keys[int(i)], words[int(j)]
        if v in level_words_kv[k]:
            result[k] = v
    return result

def get_words_level(cuts):
    resdct = {}
    cur_index = -1
    for word in cuts:
        cnt=0
        for k,reg in zip(level_keys,reg_lst):
            cnt+=1
            if cnt>2:
                cnt = 0
                break
            if level_keys.index(k)>cur_index:
                if len(re.findall(reg,word))>0 and not re.findall(reg,word)[0] =='':
                    print('正则过滤',re.findall(reg,word),k,word,reg)
                    resdct[k] = re.findall(reg,word)[0]
                    cur_index = level_keys.index(k)
                    print(cur_index)
                    pass
                    break
    print('规则过滤',resdct)
    map_resdct = dict_search(cuts)
    print('词库过滤',resdct)
    res = comb(resdct,map_resdct)
    return res

def merge(rule,xgb):
    merge = rule.copy()
    ks = ['小区名','组团名称']
    for k in ks:
        if k in rule and not k in xgb:
            pass
        elif not k in rule and k in xgb:
            merge[k] = xgb[k]
        elif k in rule and k in xgb:
            if rule[k] == xgb[k]:
                pass
            else:
                merge[k] = xgb[k]
        elif not k in rule and not k in xgb:
            pass
        else:
            raise Exception("rule xgb diff Invalid Status!")
    return merge

def cut(line):
    txt = utils.pre_trans(line)
    cuts = list(jieba.cut(txt))

def _pred(k,v,bst):
    X_train, y_train = [],[]
    X_train.append(trans(v))
    y_train.append(dct_trans(k,global_dct))
    d_pred = xgb.DMatrix(np.array(X_train).reshape(-1,myconfig.LENTH_PADDING), label=np.array(y_train).reshape(-1))
    pred = bst.predict(d_pred)
    print(pred,global_dct[k],v)
    return global_num_dct.get(pred[0],'其他')

#'''
#def new_cut_xgb(line):
#    global BST
#    '''
#    使用xgb分词器进行分词
#    '''
#    txt = utils.pre_trans(line)
#    global global_cnt
#    global_cnt+=1
#    cuts = list(jieba.cut(txt))
#    dct = {}
#    k = _pred("省",wd,BST)
#    if k in dct:
#        if wd in dct[k] or dct[k] in wd:
#            continue
#        else:
#            dct[k]+=wd
#    else:
#        dct[k] = wd
##    dct['sent'] = line
#    print('new_cut_xgb',dct)
#    return dct
#'''

def pos_cut(line):
    res = ''
    words=jieba.posseg.cut(line)
    for word in words:
        res+="%s/%s "%(word.word,word.flag)
    return res

def new_cut(line):
    global global_cnt
    global_cnt+=1
    txt = utils.pre_trans(line)
    cuts = list(jieba.cut(txt))
    rule = get_words_level(cuts)
    rule['sent'] = utils.pre_trans(line)
    print('new_cut',rule)
    return rule

if __name__ == "__main__":

  with open("cut_result.txt","a+") as g:
    with open("add_total.txt","r") as f:
        lines = f.readlines()
        np.random.shuffle(lines)
        lines = lines[:100]
        cnt = 0
        for line in lines:
            res = new_cut(line)


