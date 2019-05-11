import networkx as nx
import re
import jieba
#import address_activaty as addr_acti    
    
def init_di_graph():    
    lines = open("./data/std/gy_std_addr3.txt","r").readlines()
    dg = nx.Graph()
    for line in lines[:10]:
        lst = []
        lst.append('ROOT')
        dg.add_node('ROOT')
        line = re.sub("[\r\n]","",line)
        for word in jieba.cut(line):
            lst.append(word)
            print(lst)
            if len(lst)>1:
                if lst[-1] in nx.all_neighbors(dg,lst[-2]):
                    try:
                        w = dg[lst[-2]][lst[-1]]['weight']
                        w+=1
                        dg[lst[-2]][lst[-1]]['weight'] = w
                        continue
                    except:
                        pass
                dg.add_edge(lst[-2],lst[-1])
                dg[lst[-2]][lst[-1]]['weight'] = 1
        dg.add_edge(lst[-1],'ROOT')
    return dg
    
def load_sentence(n):
    lines = open("./data/test/gy/guiyang_2kk","r").readlines()
    return lines[:n]

def weight_sum(lst):
    _sum = 0
    for cur in range(len(lst)-1):
        _sum+=np.log(di[lst[cur]][lst[cut+1]]['weight'])
    return _sum

def weight_calc(routes):
    _min = []
    _min_value = -999
    for lst in routes:
        if weight_sum(lst)>_min_value:
            _min = lst
    return _min
        
def viterbi(words):
    res = []
    for i in range(len(words)-1):
        routes = nx.all_simple_path(di,words[i],words[i+1])
        res.append(weight_calc(routes))

if __name__ == "__main__":
    #main()
    pass

