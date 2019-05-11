#!encoding=utf8
import networkx as nx
import pdb
import traceback
import pandas as pd
import jieba
import collections
#jieba.load_userdict("/data/gensimplus/source/dct_file/matrix_add.txt")
import numpy as np
import os
import re
import trie_tree
import svm_tf
import functools
from functools import reduce
import utils

def strQ2B(ustring):
    ustring = str(ustring)
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12200:
            inside_code = 32
        elif inside_code >= 65281 and inside_code <= 65374:
            inside_code -= 65248
        rstring+=chr(inside_code)
    return rstring

def clr(strs):
    return re.sub("[^\u4e00-\u9fa5]"," ",strs)
    #return re.sub("[\da-zA-z]","",strs)

def num_filter(strs):
    return re.findall("[\da-zA-Z]+.",strs)

def rand_lst(m,n):
   return [np.random.randint(0,m) for i in range(n)]

class My_Graph(object):
    """
    """
    def __init__(self):
        self.di = nx.Graph()
        self.tree_di = nx.DiGraph()
        self.sent = {}
        self.filter_line = 30.0
        self.wealth = {}
        self.size = 256#减小hash长度，bloom过滤器
        self.num = 9999#常数项
        self.sent["-1"] = "-1"#
        self.clus_node = set()
        #self.batch = 16
        self.batch = 6000000
        self.core_value = {}
        self.tree_clus_node= set()
        self.filename = "/data/network/data/std/gy_std_addr3.txt"
        self.samples = self.get_lines(0)
        #self.bind_sentence_from_csv()
        self.bind_sentence_from_txt()
        #self.bind_sentence_from_txt(filename,self.batch)
        #self.trietreeIns = trie_tree.Trie()
        #self.init_trie_tree()
        #self.my_svm_ins = svm_tf.MySVM()
        #self.my_svm_ins.init()
        #self.my_svm_ins.run()

    def get_lines(self,cut):
        cont = open(self.filename).read()
        self.samples = cont[cut:min(len(cont),cut+10000)]

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
        cmdout = r"区"
        base = re.sub(cmdin,cmdout,src_sent)
        return base

    def filter(self,src_sent,target_sent):
        base = re.split("\d+",src_sent)[0]
        for word in jieba.cut(base):
            if word in target_sent:
                return True
        return False

    def stopword(self,sent):
        stws = ['交叉口','向[东南西北]','与','交汇','交界处','\d+米']
        for stw in stws:
            sent = re.sub("%s"%stw,"",sent)
        return sent

    def bind_word_sequence(self):
        pass

    def bind_word_with_sentence(self,sentence):
        """connect sentence to its every words"""
        #将词和句子建立图节点与边
        #c = 我爱北京 (c,我)(c,爱)(c,北京)
        sentence = sentence.strip()
        h = hash(sentence)#把句子hash
        append_lst = []
        #for word in jieba.cut(self.before_first_num(sentence)):#weight是权重，作用在于把信息量大的词找出来
        for word in jieba.cut(sentence):#weight是权重，作用在于把信息量大的词找出来
            append_lst.append(word)
            if " " in append_lst:
                append_lst.remove(" ")
            #if len(append_lst)>1:
            #    self.tree_di.add_edge(append_lst[-2],append_lst[-1],{"weight":1})
            if str(h) in self.clus_node and word in self.clus_node:
                res = self.di.get_edge_data(word,str(h))
                if not res == None:
                    wv = res['weight']#为图拓扑结构添加边,weight是权重，如果边已经存在则权重加1，也就是句子里两个相同的词，权重为2
                    wv+=1
                    self.di[word][str(h)]['weight'] = wv
                    continue
            self.di.add_edge(word,str(h))
            self.di[word][str(h)]['weight'] = 1
            self.sent[str(h)] = sentence#存到词典里用于后续还原
            self.clus_node.add(word)
            self.clus_node.add(str(h))

    def gen_csv(self,filename):
        df = pd.read_csv(filename)
        for i in df.iloc[:,1]:
            yield utils.clr(str(i).strip())
        #for i in rand_lst(len(df.iloc[:,1]),self.batch):
        #    yield utils.clr(str(df.iloc[i,1].strip()))

    def gen_txt(self,filename):
        f = open(filename,'r')
        lines = f.readlines()
        for i in rand_lst(len(lines),self.batch):
            yield strQ2B(str(lines[i].strip()))

    def bind_sentence_from_txt(self):
            # 将词和句子添加到图拓扑结构里做边，完成整个文档的添加,64G可添加100万条目,完成跑通,500万级别，添加可以，跑通出错
            """bind sentence from csv"""
            print("bind sentence from txt")
            filename = self.filename
            gen_lin = self.gen_txt(filename)
            cnt = 0
            for line in gen_lin:
                #print(line)
                self.add_tree_route(line)
                self.bind_word_with_sentence(line)
                cnt+=1
                if cnt%10000 == 1:
                    print(cnt)

    def before_first_num(self,line):
        return re.split('\d',line)[0]

    def bind_sentence_from_csv(self):
            self.di.clear()
            self.tree_di.clear()
            """bind sentence from csv"""
            df = self.gen_csv(self.filename)
            cnt = 0
            for line in df:
                self.add_tree_route(utils.clr(line))
                self.bind_word_with_sentence(utils.clr(line))
                #self.bind_word_with_sentence(self.before_first_num(line.strip()))
                cnt+=1
                if cnt%1000 == 1:
                    print("we have bind ",cnt," sentence")

    def clog(self,_log):
        return 4/np.log(10 + _log)

    def _core(self,u,v,_idx,_idy):
        _u = self.clog(self.di.degree(u))
        _v = self.clog(self.di.degree(v))
        return _u+_v

    def core(self,u,v,_idx,_idy,l):
        if "%s&%s&%s&%s"%(str(u),str(v),str(_idx),str(_idy)) in self.core_value:
            return self.core_value["%s&%s&%s&%s"%(str(u),str(v),str(_idx),str(_idy))]
        sub_index = max(_idx,_idy)-min(_idx,_idy)+1
        _u = np.log(self.batch)-np.log(self.di.degree(u))
        _ul = _u*len(u)
        _v = np.log(self.batch)-np.log(self.di.degree(v))
        _vl = _v*len(v)
        _w = self.clog(sub_index)
        #print("u:",u,"v:",v,"_u:",_u,"_v:",_v,"_w:",_w)
        self.core_value["%s&%s&%s&%s"%(str(u),str(v),str(_idx),str(_idy))] = _u+_v+_w
        if True:
            #print("submatmul",[len(u),len(v),_u,_v,self.clog(l-_idx),self.clog(l-_idy),self.clog(sub_index)])
            #_ = np.subtract(np.matmul([len(u),len(v),_u,_v,self.clog(l-_idx),self.clog(l-_idy),self.clog(sub_index)],[1.0,1.0,1.0,1.0,1.0,1.0,1.0]),[0.0])
            #_ = np.sum(np.subtract(np.matmul([len(u),len(v),_u,_v,l-_idx,l-_idy,sub_index],[1.0,1.0,0.0377,-1.3608,0.9449,1.0677,0.9134]),[0.2788]))
            print("core,",_ul,_vl,u,v)
            return (_ul+_vl)
        else:
            if _u+_v+_w>self.filter_line:
                self.my_svm_ins.step(np.array([np.log(self.di.degree(u)), np.log(self.di.degree(v)), _idx, _idy, sub_index]).reshape(1,5), np.array(1).reshape(1,1))
            else:
                self.my_svm_ins.step(np.array([np.log(self.di.degree(u)), np.log(self.di.degree(v)), _idx, _idy, sub_index]).reshape(1,5), np.array(1).reshape(1,1))
            return _u+_v+_w

    def common_neib(self,u,v,_idx,_idy):
            #find the core of tree
            #核心逻辑，计算词的共同邻居节点
            #共同邻居越多，共同邻居信息量越大，越重要,可以超越分级
            #也就是此前分级与找核心词的步骤，换一种实现方式
            if u in self.clus_node:
                if v in self.clus_node:
                    try:
                        nx.common_neighbors(self.di,u,v)
                    except:
                        #print("there is no common neightbors",u,v)
                        return -1
                    for i in nx.common_neighbors(self.di,u,v):
                        #print("u",u,"END")
                        #print("v",v,"END")
                        #print("sent",self.sent[i])
                        x = self.sent[i].index(u)
                        #print("x",x)
                        y = self.sent[i].index(v)
                        #print("y",y)
                        xsuby = max(x,y)-min(x,y)
                        l = len(self.before_first_num(self.sent[i]))
                        _uv = self.core(u,v,x,y,l)
                        #_uv = np.log(_uv)-np.log(sub_index+1)
                        #位置越靠前越重要，节点的度越少越重要,_idx代表位置，degree代表度
                        #uv是词,i是uv的公共邻居句子
                        if i in self.wealth:
                            self.wealth[i]+=_uv
                            #self.wealth[i] = max(self.wealth[i],_uv)
                        else:
                            self.wealth[i]=_uv
                        #if _uv > 3:
                        #print("> common_neib",i,u,v,_uv)

    def show_wealth(self,sent):
        #计算评分
        for k in sorted(self.wealth.items(), key=lambda d: d[1],reverse=True)[:3]:
            print(sent, self.sent[k[0]], self.wealth[k[0]])

    def add_tree_route(self,sentence):
            wdlst = []
            #for word in jieba.cut(self.before_first_num(sentence)):
            for word in jieba.cut(sentence):
                wdlst.append(word)
                if len(wdlst)>1:
                    if wdlst[-2] in self.tree_clus_node and wdlst[-1]in self.tree_clus_node:
                        res = self.tree_di.get_edge_data(wdlst[-2],wdlst[-1])
                        if not res == None:
                            wv = res['weight']
                            wv+=1
                            self.tree_di[wdlst[-2]][wdlst[-1]]['weight'] = wv
                            continue
                    self.tree_di.add_edge(wdlst[-2],wdlst[-1])
                    self.tree_di[wdlst[-2]][wdlst[-1]]["weight"] = 1
                    self.tree_clus_node.add(wdlst[-2])
                    self.tree_clus_node.add(wdlst[-1])

    def compare(self):
        print("compare")
        for _,_,filename_ins in os.walk("/data/network/data/test/gy"):
            for filename_in in filename_ins:
                #ni#print(filename_in)
                #df = pd.read_csv(os.path.join("/data/network/data/test/gy",filename_in))
                _path = os.path.join("/data/network/data/test/gy",filename_in)
                #print(_path)
                lines = open(_path).readlines()
                df = pd.DataFrame(np.array([lines,lines]).reshape(len(lines),2))
                with open ("/data/network/data/predict/record.txt","a+") as f:
                    for _l in rand_lst(len(df.iloc[:,1]),len(df.iloc[:,1])):
                        _line = df.iloc[_l,1]
                        _line = strQ2B(str(_line).strip())
                        #print(_line)
                        number_lst = num_filter(_line)
                        _line = self.cut_filter(_line)
                        results = self.run_sent(self.stopword(_line))
                        #print(results)
                        for result in results:
                            number_lst_k0 = num_filter(result)
                            if len(number_lst)>0 and len(number_lst_k0)>0:
                                l = min(len(number_lst_k0),len(number_lst))
                                l = min(2,l)
                                #print(result,_line)
                                if number_lst_k0[:l] == number_lst[:l]:
                                    f.write(_line+'\t'+ result +"\n")
        self.di.clear()
        self.tree_di.clear()
        self.clus_node = set()

    def treescan(self,reslst):
        """ the words is all the connection posibility between two words"""
        for words in reslst:
            pass

    def search(self):
        for _,_,filename_ins in os.walk("/data/network/data/test/gy"):
            for filename_in in filename_ins:
                #print(filename_in)
                #filename_in = "dz_zzxx_cs_4.csv"
                _path = os.path.join("/data/network/data/test/gy",filename_in)
                #print(_path)
                df = open(_path).readlines()
                with open ("/data/network/data/predict/record.txt","a+") as f:
                    for _l in rand_lst(len(df),self.batch):
                        _line = df[_l]
                        _line = strQ2B(str(_line).strip())
                        _line = self.cut_filter(_line)
                        number_lst = num_filter(_line)
                        reslst = self.run_sent_from_graph(self.before_first_num(self.stopword(_line)))
                        if len(reslst)==0:
                            continue
                        #tree_route = self.treescan(reslst,trietreeIns)
                        hashlst = self.query_in_set(reslst)
                        for hs in hashlst:
                            number_lst_k0 = num_filter(hs)
                            if len(number_lst)>0 and len(number_lst_k0)>0:
                                l = min(len(number_lst_k0),len(number_lst))
                                l = min(2,l)
                                if number_lst_k0[:l] == number_lst[:l]:
                                    f.write(_line+'\t'+ hs +"\n")
        self.di.clear()
        self.tree_di.clear()
        self.clus_node = set()

    def query_in_set(self, sentences):
        st = []
        results = []
        for words in sentences:
            if len(words)>1:
                cmd=".*?"
                cmd+=".*".join(words)
                cmd+=".*?"
            else:
                continue
                cmd=".*?"
                cmd+=words
                cmd+=".*?"
            res = re.findall(cmd,self.samples)
            print("query once",cmd)
            if len(res)>0:
                results.extend(list(res))
                print(cmd,line,results)
        return results

    def set_join_line(self, sentences):
        st = []
        results = []
        for words in sentences:
            for i,j in zip(words[:-1],words[1:]):
                try:
                    nx.common_neighbors(self.di,i,j)
                except:
                    print(i,j,"has not common neighbor")
                    break
                _ = list(nx.common_neighbors(self.di,i,j))
                print(_)
                st.append(_)
            if len(st)>0:
                result = reduce(lambda x,y:x+y, st)
                print(result)
                result = dict(collections.Counter(result))
                #_out = sorted(result.items(), key=lambda d: d[1],reverse=True)[:min(3,len(result))]
                for _ in result:
                    if result[_]>1:
                        results.append(_)
        return results

    def combine(self,x,y):
        res = []
        if len(x) > 0:
            if len(y) > 0:
                for xx in x:
                    for yy in y:
                        if xx == "":
                            xxyy = xx+yy
                        else:
                            xxyy = xx+yy[1:]
                        res.append(xxyy)
            else:
                res = x
        else:
            res = y
        return res

    def run_sent_from_graph(self,insentence):
        #评测某个句子
        #if len(re.findall("\d+",sentence))>0:
        #    sentence = sentence.split("\d")[0]
        self.wealth = {}
        #print(insentence)
        #insentence = re.sub("[^\u4e00-\u9fa50-9a-zA-Z]"," ",str(insentence))
        wdlst = []
        res = []
        for word in jieba.cut(self.before_first_num(insentence)):
            if " " == word:
                continue
            wdlst.append(word)
            if len(wdlst)>1:
                try:
                    res.append(list(nx.all_shortest_paths(self.tree_di,wdlst[-2],wdlst[-1])))
                    #print(res)
                except:
                    wdlst = wdlst[:-1]
                    continue
        #print("res", res, "res")
        _resbind = []
        for lst in res:
            _resbind = self.combine(_resbind, lst)
        #print(_resbind)
        return _resbind

    def run_sent(self,_insentence):
        #评测某个句子
        #if len(re.findall("\d+",sentence))>0:
        #    sentence = sentence.split("\d")[0]
        insentence = self.before_first_num(_insentence)
        # insentence = _insentence
        #insentence = re.sub("[^\u4e00-\u9fa5]"," ",insentence)
        #print(insentence)
        self.wealth = {}
        sentence = list(jieba.cut(clr(insentence)))
        if " " in sentence:
            sentence.remove(" ")
        for p in range(0,len(sentence)):
            for q in range(0,len(sentence)):
                if q<p or q==p:
                    continue
                i = sentence[p]
                j = sentence[q]
                self.common_neib(i,j,p,q)
                #print(i,j,p,q)
        self.show_wealth(sentence)
        #print(sentence, self.wealth)
        if self.wealth == {}:
            #print("there is no common neighbor between this two word")
            return ["-1"]
        _out = sorted(self.wealth.items(), key=lambda d: d[1],reverse=True)
        #_out = sorted(self.wealth.items(), key=lambda d: d[1],reverse=True)[:min(3,len(self.wealth.items()))]
        _out_lst = []
        for _id in _out:
            if _id[1] < self.filter_line:
               continue
            #if self.filter(insentence,self.sent[_id[0]]):
            #    _out_lst.append(self.sent[_id[0]])
            #    return _out_lst
            _out_lst.append(self.sent[_id[0]]+"\t"+str(_id[1]))
        if len(_out_lst)>0:
            return _out_lst
        return ["-1"]

if __name__ == "__main__":
    line = "河南省中牟县广惠街街道办事处商都大道150号6号楼"
    line2 = "河南省新郑市新建路街道办事处褚庄四巷19号"
    mg = My_Graph()
    while(1):
        cnt=0
        for i in range(100):
            mg.get_lines(cnt*10000)
            mg.search()
            cnt+=1
            #mg.compare()
        mg.bind_sentence_from_txt()

