import re
import numpy as np
import time
import json

rules = ["层","[东西南北]户","交汇处","与","号院","楼梯","号","单元", "楼", "[\da-zA-Z]+?号[楼院]?","[\d一-十]+?单元", "\d+层", "\d+室", "\d+户", "\d+排", "商铺", "[\da-zA-Z]+?栋", "[东南西北]$", "[东南西北]户$", "[\da-zA-Z]+?楼", "[^\u4e00-\u9fa5]+"]

comp_rules = []
for rule in rules:
    comp_rules.append(re.compile(rule))

def is_max(input_item,max_value):
    return input_item[1] == max_value

def rand_lst(m,n):
   return [np.random.randint(0,m) for i in range(n)]

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
    #return re.sub("[^\u4e00-\u9fa50-9A-Za-z]","",rstring)
    return rstring

def get_nums(line):
    return "C".join(re.findall("\d+",line))

def get_chars_nums(line):
    return "C".join(re.findall("[\da-zA-Z]+",line))

def clr(line):
    _line = strQ2B(line)
    #line = re.sub("与.+?交叉.+?米","",line)
    #line = re.sub("[^u4e00-\u9fa5a-z0-9A-Z]","",line)
    #_line = line.strip()
    return _line

def without_num(line):
    line = strQ2B(line)
    for rule in comp_rules:
      line = re.sub(rule," ",line)
    return line

def before_first_num(line):
    return re.split("\d+",line)[0]

def numbers(line):
    return re.findall("\d+",line)

def first_numbers(line):
    nums = re.findall("\d+",line)
    if len(nums)>0:
        return nums[0]
    return ""

def weight_sum(lst_sum):
    weightlst = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536]
    if len(lst_sum) == 0:
        return 0
    cnt = 0
    _sum = 0
    for i in lst_sum:
        weight = weightlst[min(cnt,len(weightlst)-1)]
        cnt+=1
        _sum+=(i*weight)
    return np.log(_sum)

def _weight_sum(lst_sum):
    weights = [1,2,3,4,7,11,18,29,47,76,123,199,322,521]
    lst_sum = lst_sum[::-1]
    weights = weights[:len(lst_sum)]
    p = map(lambda x,y:x*y, weights,lst_sum)
    return np.log(1+np.sum(list(p)))

def compare_num(sm,sn):
    score = 0
    _p = numbers(sm)
    _a = numbers(sn)
    ml = min(len(_p),len(_a))
    if ml == 0:
        return score
    for i,j in zip(_p[:ml],_a[:ml]):
        if str(i) == str(j):
            score+=1
            continue
        return score
    return score

def minEditDist(sm, sn):
    lst_sum = []
    score = 0
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
                score += 1
            else:
                cost = 1
                return score
            matrix[i][j] = min(matrix[i-1][j]+1,matrix[i][j-1]+1,matrix[i-1][j-1]+cost)
            lst_sum.append(cost)
    return score

def add_sent_2_word(r,word,senthash):
  r.sadd('%s'%word,'%s'%senthash)
  return 0
 
def get_sent_from_word(r,word):
  return r.smembers('%s'%word)
	
def get_common_neighbor(r,word1,word2):
  #print("计算公共邻居redis测试", time.time())
  ret = r.sinter('%s'%word1, '%s'%word2)
  #print("计算公共邻居redis测试,计时",time.time())
  #print(ret)
  return ret

def sav_json(model):
    with open("./degree.json",'w',encoding='utf-8') as json_file:
        json.dump(model,json_file,ensure_ascii=False)
  
def load_json():
    model = {}
    with open("./degree.json",'r',encoding='utf-8') as json_file:
        model=json.load(json_file)
        return model

def BFS_hungary(g,Nx,Ny,Mx,My,chk,Q,prev):
    res=0
    for i in xrange(Nx):
        if Mx[i]==-1:
            qs=qe=0
            Q[qe]=i
            qe+=1
            prev[i]=-1

            flag=0
            while(qs<qe and not flag):
                u=Q[qs]
                for v in xrange(Ny):
                    if flag:continue
                    if g[u][v] and chk[v]!=i:
                        chk[v]=i
                        Q[qe]=My[v]
                        qe+=1
                        if My[v]>=0:
                            prev[My[v]]=u
                        else:
                            flag=1
                            d,e=u,v
                            while d!=-1:
                                t=Mx[d]
                                Mx[d]=e
                                My[e]=d
                                d=prev[d]
                                e=t
                qs+=1
            if Mx[i]!=-1:
                res+=1
    return res
