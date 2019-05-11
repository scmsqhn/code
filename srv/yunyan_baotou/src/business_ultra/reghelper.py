#!/usr/bin/env python3
import datetime
import pandas as pd
import pdb
from datetime import datetime
import json
import my_helper
import sys
import os
sys.path.append(os.environ['YUNYAN'])
print(os.environ['YUNYAN'])
import myconfig
import myjieba_posseg
import myjieba_posseg.posseg as posseg
#myjieba_posseg.add_word("上海",999,"CITY")
#print(list(myposseg.cut('北京西城区')))
#print(list(posseg.cut('北京西城区')))

import function_ultra.utils as utils
import function_ultra.utils_bt as utils_bt
#import function_ultra.utils_back_trans as ubt
import os
import codecs
import numpy as np
import traceback
import sys
import gensim
#from gensimplus.source.gensim_plus_config import FLAGS
#from gensimplus.source.model_save_load_helper import ModelSaveLoadHelper
from gensim.models import LsiModel
from gensim.models import LdaModel
from gensim.models import TfidfModel
import function_ultra.trie_tree as trie_tree
sys.path.append('./business_ultra/')
from src import myjieba_posseg as jieba
#import myjieba as jieba
import re
import numpy as np
import pdb
import codecs
import myconfig
CURPATH = os.path.dirname(os.path.realpath(__file__))
#print(myjieba_posseg.__dict__)
#myjieba_posseg.load_userdict(myconfig.DICT)
print('load_userdict  dict.txt ', myconfig.DICT)

import user_prob
from user_prob.test import new_cut
from user_prob.test import pos_cut
#from user_prob.test import new_cut_xgb
DICT = False#$True
DEBUG = True
JIEBACUT= True
global r_cnt
global w_cnt
r_cnt = 1
w_cnt = 0
standard_addr = {}

load_json = lambda x:json.load(open(x,'r',encoding='utf-8'))

standard_addr = load_json(os.path.join(myconfig.DATPATH,"standard_addr.json"))

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

level_keys = ["省","市","区","社区","村居委会","街路巷名","自然村组",\
              "门牌号","小区名","建筑物名称","组团名称","栋号",\
              "单元号","楼层","户室号","sent","rw"]

out_keys = ["省","市","区","社区","村居委会","街路巷名","自然村组","门牌号","小区名","组团名称","栋号","单元号","楼层","户室号"]

global global_cnt
#import struct_ultra
#import struct_ultra.struct_interface_ultra.Singleton as Singleton
'''
class Singleton(object):

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            org = super(Singleton, cls)
            cls._instance = org.__new__(cls, *args, **kw)
        return cls._instance
'''
def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton

@Singleton
class RegHelper(object):

    def __init__(self,s):
        """
        lst = ['省','市','区','社区','居委会','自然村组','街路巷','门牌号', '建筑物名称','组团名称','楼层','栋号','楼栋名称','单元','楼层','户号']
        """
        pass #print("\n> 实例化一个新的 TfidfHelper")
        self.reg_pools = []
        self.reg_pools_part_2 = []
        CURPATH = os.path.dirname(os.path.realpath(__file__))
        self.s = s
        #self.rulelst = utils.init_rule_lst()

    def __str__(self):
        return self.s

    def create_reg_from_doc(self,docpath):
        """
        """
        f = codecs.open(docpath,"r","utf-8")
        lines = f.readlines()
        for line in lines:
            line = re.sub("[\n\r ]","",line)
            parts = line.split("aaa")
            if not len(parts) == 2:
                continue
            p0 = parts[0].split(",")
            p1 = parts[1].split(",")
            if not len(p0) == len(p1):
                continue
            p1.insert(0,self.reg_gene(p0))
            self.reg_pools.append(p1)
        f.close()

    def reg_gene(self,txtLst):
        regexp = ""
        for i in txtLst:
            if i in ['散居','[幢栋]','单元','楼','号','号','附\d号','附\d+号','栋']:
                regexp+="([附付\d甲乙丙丁戊一二三四壹贰叁肆五六七八九十a-zA-Z-]{1,7}%s)"%i
            elif i in [r'\d',r'\d+',r'(?:\d|号)']:
                regexp+="(\d+%s)"%i
            elif i in ['镇','村','组']:
                regexp+="(.{1,4}%s(?!居委会))"%i
            elif i in ['路','道','巷','街','[街道路巷段]','[街路巷道]','[街道路巷]','[街路巷道段]']:
                regexp+="([^村]{1,4}%s(?!(?:服务中心|社区服务中心|商业步行街)))"%i
            elif i in ['市','省','县','乡','镇']:
                regexp+="(.{1,7}%s)"%i
            elif i in ['委会']:
                regexp+="(.{1,7}(?:委会|委会服务中心))"
            elif i in ['区']:
                regexp+="(.{1,7}(?:(?<!i[小社])区(?!服务中心)))"
            else:
                regexp+="(.{1,7}%s)"%i
        #pass #print(regexp)
        return "^"+regexp+"[\r\n]*?$"

    def reg_factory(self,intxt):
        kw = "省市区路号社区栋乡镇县幢单元楼层号室乡村组寨坡"
        outtxt = re.sub("[^%s]"%kw,"",intxt)
        return outtxt

    def part_ext(self,txt,pat,target,resdict):
            if txt == "":
                return resdict
            #pass #print(target)
            res = re.findall(pat,txt)
            if len(res)<1:
                pass #print("无法拆分")
                resdict['other'] = txt
                return resdict
            #pass #print(res)
            [result,other] = list(res[0])
            resdict['other'] = other
            resdict[target] = result
            #pass #print("====")
            return resdict

    def address_formula_sub(self,txt):
        #pass #print(datetime.now())
        try:
            """
            对于精确匹配的数据 进行分级匹配 逐步明确地址分类
            主要用于面向除去常口和社区警务的住建水电器等地址
            self.reg_pools_part_2.append([pattern,"省","市","区","社区","村居委会","街路巷名","自然村组","门牌号","小区名","建筑物名称","组团名称","楼号","栋号","单元号","层","户室号"])
            """
            pass

            resdict = {}
            resdict['other'] = txt
            resdict = self.part_ext(resdict['other'],sheng,"省",resdict)
            resdict = self.part_ext(resdict['other'],shi,"市",resdict)
            resdict = self.part_ext(resdict['other'],qu,"区",resdict)
            resdict = self.part_ext(resdict['other'],shequ,"社区",resdict)
            resdict = self.part_ext(resdict['other'],cunjuweihui,"村居委会",resdict)
            resdict = self.part_ext(resdict['other'],zirancunzu,"自然村组",resdict)
            resdict = self.part_ext(resdict['other'],jieluxiang,"街路巷名",resdict)
            resdict = self.part_ext(resdict['other'],menpaihao,"门牌号",resdict)
            #xiaoqu = re.compile(r'([^一二三四壹贰叁肆五六七八九十散附\d单元甲乙丙丁戊a-zA-Z]+(?:小区|园|苑|[首一二三四壹贰叁肆五六七八九十]期|花园|山美诗|方舟|城|居住区|新城|院|[\u4e00-\u9fa5])?(.+)?')
            #xiaoqu = re.compile(r'(.+?)?(?<!栋)(?<!期)(?<!号)(?<!\d)(?<![楼栋])(?<![单元])(?=[a-zA-Z\d一二三四甲乙丙丁壹贰叁肆])(.+)?')
            resdict = self.part_ext(resdict['other'],xiaoqu,"小区名",resdict)
            resdict = self.part_ext(resdict['other'],jianzhuwu,"建筑物名称",resdict)
            resdict = self.part_ext(resdict['other'],zutuan,"组团名称",resdict)
            #resdict = self.part_ext(resdict['other'],louhao,"楼号",resdict)
            resdict['other'] = re.sub("杠","-",resdict['other'])
            resdict = self.part_ext(resdict['other'],donghao,"栋号",resdict)
            resdict = self.part_ext(resdict['other'],danyuan,"单元号",resdict)
            resdict = self.part_ext(resdict['other'],louceng,"楼层",resdict)
            #hushihao = re.compile(r'((?:[\da-zA-Z]+型)?正?(?:[\da-zA-Z]+)?[负附付夹底夹底地下层]*?[门面\da-zA-Z\-、]+[号幢室]+?(?:附[\d一二三四壹贰叁肆五六七八九十]+?号)?|\d+号|\d+|附?[\d一二三四壹贰叁肆五六七八九十]+号门面|[a-zA-Z]座|\d+0\d+)?(?:空挂户)?(.*$)?[\r\n]$')
            #resdict = self.part_ext(resdict['other'],hushihao,"户室号",resdict)
            resdict['户室号'] = resdict['other']
            resdict.pop('other')
            return resdict
        except:
            traceback.print_exc()
            if DEBUG:
                with open("./logs.txt","a+") as f:
                    s = traceback.print_exc()
                    f.write("%s\n"%s)
                    #pdb.set_trace()

    def txt_reformat(self,txt):
        pass #print(txt)
        sents = txt.split(',')
        sent0 = sents[0]
        kvs = sents[1:]
        sent0 = re.sub("[^\u4e00-\u9fa50-9a-zA-Z]","",sent0)
        js = {}
        js['sent'] = sent0
        for sent in kvs:
            pass #print(sent)
            if not ":" in sent:
                continue
            k,v = sent.split(':')
            k = re.sub("[^\u4e00-\u9fa50-9a-zA-Z]","",k)
            v = re.sub("[^\u4e00-\u9fa50-9a-zA-Z]","",v)
            js[k] = v
        return js

    def comp(self,baselabel,outbase,f):
        for k in baselabel:
            if k == 'sent':
                continue
            if k in outbase:
                if not outbase[k] == baselabel[k]:
                    f.write('WRONG%s\n'%baselabel['sent'])
                    return 0
            else:
                f.write('WRONG%s\n'%baselabel['sent'])
                return 0
        f.write('RIGHT%s\n'%baselabel['sent'])
        return 0
    
    def posseg_cut(self,original_sentence):
        #delimeter = ' '
        # original_sentence为原始地址
        #print('\n>多源词性标注:',delimeter.join(list(myposseg.posseg.cut(original_sentence))))
        #pdb.set_trace()
        result = ""
        words = list(posseg.cut(original_sentence))
        for word in words:
            result+="%s/%s "%(word.word, word.flag)
        print(result)
        return result

    def __address_formula(self,original_sentence):
        # original_sentence为原始地址
        #trans_sentence = ubt.pre_trans(original_sentence)  # 规则转化地址, 以及对应的转化信息
        trans_sentence = original_sentence
        split_result = self.base_address_formula(original_sentence)  # 切分
        print('split_result',split_result)
        other = split_result.get('other','')
        #split_result格式：{original_sentence: {'区':, '单元号':, '小区名':,...}}
        split_result = {original_sentence:split_result}
        #split_final_result = ubt.split_final(trans_sentence,split_result)  # 还原切分结果
        split_final_result=split_result
        sent_base = list(split_final_result.items())[0][0]
        result = list(split_final_result.items())[0][1]
        result['sent'] = sent_base
        result['other'] = other
        print('result', result)
        ret = ''
        for k in result:
            v = result.get(k)
            if v == '':
                ret+=' DUMMY/%s'%k
            else:
                ret+=' %s/%s'%(v,k)
        return ret

    def address_formula(self,sentence):
        # original_sentence为原始地址
        #trans_sentence = ubt.pre_trans(original_sentence)  # 规则转化地址, 以及对应的转化信息
        words = my_helper.address_formula(sentence)
        #res = utils_bt.pre_trans(sentence)
        #line = list(res.keys())[0]
        #words = posseg.my_jieba_cut(line)
        return words
        #pdb.set_trace()
        #result = ""
        #for word in words:
        #    item = "%s/%s "%(word.word, word.flag)
        #    result+=item
        #return result

    def base_address_formula(self,txt):
        #txt = re.sub("(.+?)[\(（].+?[\)）]","\1",txt)
        #txt = re.sub("\(.+?\)","",txt)
        #txt = re.sub("（.+?）","",txt)
        #txt = re.sub("[^\u4e00-\u9fa50-9a-zA-Z\-]","",txt)
        global global_cnt
        maxlen = 0
        base,outbase = {},{}
        base_exp = ""
        base= {}
        txt = utils.pre_trans(txt)
        #base= new_cut_xgb(txt)
        base= {}
        base_rule= new_cut(txt)
        out = self.complex(base,base_rule)
        print('new_cut',out)
        outbase = self.double_check(out)
        outbase['rw'] = "0"
        global w_cnt
        global r_cnt
        if outbase['rw'] == "1":
            w_cnt+=1
        else:
            r_cnt+=1
        #keys = ["省","市","区","社区","村居委会","街路巷名","自然村组","门牌号","小区名","组团名称","楼号","栋号","单元号","楼层","户室号","rw",'sent']
        out_set = {}
        for k in level_keys:
            out_set[k] = outbase.get(k,'')
        pass #print(out_set)
        out_set['楼号'] = ''
        #out_set['省'] = '河南省'
        print('out_set',out_set)
        return out_set

    def write_2_csv(self,outbase,keys):
        with open("check.csv","a+") as f:
            sent = ""
            for k in keys:
                if k in outbase:
                    sent+="%s,"%outbase[k]
                else:
                    sent+=","
            pass #print(sent)
            f.write("%s\n"%sent)

    def write_2_jieba(self,outbase):
        with open("jieba_cut_cont.txt","a+") as f:
            for k in outbase:
                if k=="sent":
                    continue
                elif k=="rw":
                    continue
                else:
                    f.write("%s\n"%outbase[k])

    def cell_formula(self,restr):
        formula_restr = self.cell_forumula(restr)

    def ifin(self,txt,dct,classify):
        pass
        if  txt in dct['sent']:
            try:
                if txt in dct[classify]:
                    return True
            except KeyError:
                return False
        else:
            return True
        return False

    def double_check(self,inbase):
        pass #print('double_check',inbase)
        base = inbase.copy()
        kws = ['other','组团名称','建筑物名称','小区名','省','市','区','社区','村居委会','自然村组','栋号','楼层','户号','单元号','门牌号','街路巷名']
        mapkv = {}
        mapkv['[街路巷道段]'] = "街路巷名"
        mapkv['街路巷'] = "街路巷名"
        mapkv['服务中心'] = "社区"
        mapkv['委会'] = "村居委会"
        mapkv['街路巷道'] = "街路巷名"
        mapkv['街道路巷'] = "街路巷名"
        mapkv['建筑物'] = "建筑物名称"
        mapkv['建筑物名'] = "建筑物名称"
        mapkv['巷'] = "街路巷名"
        mapkv['道'] = "街路巷名"
        mapkv['街区'] = "街路巷名"
        mapkv['路'] = "街路巷名"
        mapkv['段'] = "街路巷名"
        mapkv['号'] = "门牌号"
        mapkv['乡'] = "社区"
        mapkv['镇'] = "社区"
        mapkv['村'] = "村居委会"
        mapkv['组'] = "自然村组"
        mapkv['县'] = "区"
        mapkv['栋'] = "栋号"
        mapkv['幢'] = "栋号"
        mapkv['层'] = "楼层"
        mapkv['楼'] = "楼层"
        mapkv['单元'] = "单元号"
        mapkv['室'] = "户室号"
        mapkv['社'] = "村居委会"
        mapkv['公司'] = "小区名"
        mapkv['组(?!团)'] = "自然村组"
        mapkv['社区服务中心'] = "社区"
        mapkv['[街路巷爱道]'] = "街路巷名"
        mapkvLst = [str(k) for k in mapkv]
        for k in inbase:
            if k in mapkvLst:
                v = mapkvLst.get(k,k)
                base[v] = base[k]
                base.pop(k)
            else:
                v = k
            if v == "市":
                '''
                主要针对清镇市类似词进行修改,避免县级市分如地级市
                '''
                if base[v] in ["贵阳","贵阳市","六盘水","六盘水市","遵义市","遵义","安顺","安顺市","铜仁","铜仁市","毕节市","毕节",""]:
                    pass
                else:
                    base['区'] = base[v]
                    base.pop(v)
        print('base',base)
        return base

    def xiaoqu_check(self,outbase):
        tmp = outbase.copy()
        for item in outbase:
            for name in xiaoqu_names:
                if name in outbase[item]:
                    if "居委会" in outbase[item] or "中心" in outbase[item] or "办事处" in outbase[item]:
                        return tmp
                    #tmp[item] = re.sub(name,"",outbase[item])
                    tmp["小区名"] = name
        return tmp

    def rules_cover_cnt(self,rule):
        cnt = 0
        with open("/home/distdev/iba/dmp/gongan/address_formula/data/address2.txt","r") as f:
            lines = f.readlines()
            #np.random.shuffle(lines)
            for line in lines:
                #pdb.set_trace()
                res=re.findall(rule[0],line)
                if len(res)>0:
                    cnt+=1
        #pass #print(cnt, rule[0])

    def wr_lst(self,lst,filename):
        pass
        if DEBUG:
            with open(filename,'a+') as f:
                for line in lst:
                    f.write(line)
                    f.write("\n")

    def chunked_sents(self):
        rt = []
        wr = []
        filename = "/home/distdev/iba/dmp/gongan/address_formula/address_formula.json"
        if DEBUG:
            with open(filename,"r") as f:
                cont = f.read()
                kv = json.loads(cont)
                for k in kv:
                    if len(wr)>10:
                        break
                    #pdb.set_trace()
                    sent = kv[k]['sent']
                    reskv = self.address_formula(sent)
                    for kk in kv[k]:
                        try:
                            reskv[kk]
                        except KeyError:
                            wr.append(sent)
                            break
                        if kk == "sent":
                            continue
                        elif kv[k][kk] == reskv[kk]:
                            pass
                        else:
                            wr.append(sent)
                            wr.append(kv[k][kk])
                            wr.append(reskv[kk])
                            wr.append("====")
                            break
                    rt.append(sent)
            self.wr_lst(wr,"./wrong_result.txt")
            #pass #print(len(rt),len(wr),100*len(wr)/len(rt))
        return wr,rt

    def judge(self,k,vin,vout):
        '''
        vin xgb
        vout rule
        '''
        vin = utils.pre_trans(vin)
        vout = utils.pre_trans(vout)
        v = ''
        if k in ['sent']:
            return vin
        if vin == vout:
            return vin
        print('diff', k, '-', vin, '-', vout)
        if vout == '':
            v = vout
        else:
            v = vout
        v = re.sub("栋栋","栋",v)
        v = utils.pre_trans(v)
        if '郑州' in v or '郑州市' in v or '河南省' in v  or '河南' in v:
            return ''
        return v

    def complex(self,dctin,dctout):
        res_dct = {}
        for k in level_keys:
            vin = dctin.get(k,'')
            vout = dctout.get(k,'')
            if vin == vout:
                res_dct[k] = vin
                continue
            else:
                rs = self.judge(k,vin,vout)
                res_dct[k] = rs
        return res_dct

    def isDiff(self,dctin,dctout):
        for k in level_keys:
            vin = dctin.get(k,'')
            vout = dctout.get(k,'')
            if k in ['rw','户号','户室号','省']:
                continue
            if k in ['rw','户号','户室号']:
                _vin = re.sub('[\u4e00-\u9fa5]','',vin)
                _vout = re.sub('[\u4e00-\u9fa5]','',vout)
                if _vin == _vout:
                    continue
            if vin == vout:
                continue
            return False
        return True


    def eval_one(self,dctin,f2):
            #pass #print(dctin['sent'])
            kv = {}
            kv = self.address_formula(dctin.get('sent',''))
            kv['sent'] = dctin.get('sent','')
            flag = self.isDiff(dctin,kv)
            if len(kv) == 1:
                self.wr_lst([str(kv)],"eval_score.txt")
                self.wr_lst([str(dctin)],"eval_score.txt")
                self.wr_lst([kv['sent']],"eval_score.txt")
                return flag
            return flag

    def show_diff(self,item,pred,sent):
        with open('diff_cur.txt','a+') as g:
            for k in level_keys:
                if k == 'rw':
                    continue
                value_sample = item.get(k,'')
                value_pred = pred.get(k,'')
                if not value_sample == value_pred:
                    line = k+' '+'lb:'+value_sample+'pred:'+value_pred+'sent:'+sent+'\n'
                    print(line)
                    g.write(line)

    def eval_file(self,f2):
            rcnt,wcnt = 0.0,0.0
            if True:#$DEBUG:
                #with open(os.path.join(CURPATH,"eval_1227.json"),"r") as f:
                #with open(os.path.join(CURPATH,"eval_file_1228.json"),"r") as f:
                with open(os.path.join(CURPATH,"address_formula.json"),"r") as f:
                    cont = json.loads(f.read())
                    klst = [k for k in cont]
                    np.random.shuffle(klst)
                    for k in klst:
                        item = cont[k]
                        if  "城基路" in item.get('sent','') or "鼎益市场" in item.get('sent',''):
                        #    #pdb.set_trace()
                            continue
                        if item.get('自然村组','') == "服务中心金关村":
                            continue
                        if item.get('社区','') == "电子商务园小区":
                            continue
                        if item.get('社区','') == "高天小区":
                            continue
                        if item.get('街路巷名','') == '百花大道5号':
                            continue
                        if item.get('社区','') == '沙河花园a':
                            continue
                        pass #print("input",item)
                        _item = {}
                        for i in item:
                            j = utils.pre_trans(item[i])
                            _item[i] = j
                        flag = self.eval_one(_item,f2)
                        if flag:
                            rcnt+=1.0
                        else:
                            wcnt+=1.0
                            self.wr_lst(['\n','原文',str(item),'\n'],"eval_score.txt")
                            cut_result = self.address_formula(item['sent'])
                            self.wr_lst(['\n','预测',str(cut_result),'\n'],"eval_score.txt")
                            self.show_diff(item,cut_result,item['sent'])
                        if wcnt %1 == 0:
                            pass #print(rcnt, wcnt)
                            pass
                        acc = rcnt/(rcnt+wcnt+0.1)
                        print(rcnt, wcnt, acc)

def eval(save_file):
    '''
    使用打分程序对于结果进行检验
    '''
    regHelperInstance = RegHelper('dummy')
    regHelperInstance.eval_file(open(save_file,'a+'))

def save_data(js,f):
    f.write("%s\n"%'NEXT')
    for k in js:
        f.write("%s\t%s\n"%(k,js[k]))

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

def test_zhujian():
    init_jieba()
    jieba.add_word('北京市',1)
    f = open('./zhujian.txt','a+')
    regHelperInstance = RegHelper('dummy')
    lines = open(myconfig.ZHUJIANPATH,'r').readlines()
    for line in lines:
        words = jieba.cut(line)
        for word in words:
            f.write("%s\n"%word)
        res = regHelperInstance.address_formula(line)
        f.write(str(res)+'\n')


def test_address_formula():
    lines = open('../../data/baotou_std_addr_base.txt','r').readlines()
    g = open('./result.txt','w+')
    for line in lines:
      try:
        res = utils_bt.pre_trans(line)
        line = list(res.keys())[0]
        print(posseg.cut(line))
        regHelperInstance = RegHelper('dummy')
        result = regHelperInstance.address_formula(line)
        g.write("%s\n"%result)
        g.flush()
        print('\r> result', result)
      except:
        continue
    g.close()
   
if __name__ == "__main__":
    test_address_formula()

