import networkx as nx
dig = nx.DiGraph()
dig.add_node()?
dig.add_node?
lines = open('/home/siy/data/广电全量地址_weak.csv','r').readlines()
for line in lines:
    for char in line:
        if dig.has_node(char):
            dig.node[char]['weight']+=1
        else:
            dig.add_node(char,'weight'=1)
for line in lines:
    for char in line:
        if dig.has_node(char):
            dig.node[char]['weight']+=1
        else:
            dig.add_node(char)
dig.add_node?
for line in lines:
    for char in line:
        if dig.has_node(char):
            dig.node[char].weight+=1
        else:
            dig.add_node(char, weight=1)

dig = nx.DiGraph()
for line in lines:
    for char in line:
        if dig.has_node(char):
            dig.node[char].weight+=1
        else:
            dig.add_node(char, weight=1)

dig = nx.DiGraph()
for line in lines:
    for char in line:
        if dig.has_node(char):
            print(dig.node(char))
        else:
            dig.add_node(char, weight=1)
dig.node['人']
dig.node['人']['weight']+=1

dig = nx.DiGraph()
for line in lines:
    for char in line:
        if dig.has_node(char):
            dig.node[char]['weight']+=1
        else:
            dig.add_node(char, weight=1)

dig = nx.DiGraph()
for line in lines:
    for index in range(len(lines)-1):
        dig.add_edge?
#        lines[index]

dig = nx.DiGraph()
for line in lines:
    char0 = ''
    for char in line:
        if dig.has_node(char):
            dig.node[char]['weight']+=1
        else:
            dig.add_node(char, weight=1)
        if char0==''
            char0=char
        else:
            if dig.has_edge(char0, char):
                dig.edges(char0, char)+=1
            else:
                dig.edges(char0, char)=1

dig = nx.DiGraph()
for line in lines:
    char0 = ''
    for char in line:
        if dig.has_node(char):
            dig.node[char]['weight']+=1
        else:
            dig.add_node(char, weight=1)
        if char0=='':
            char0=char
        else:
            if dig.has_edge(char0, char):
                dig.edges(char0, char)+=1
            else:
                dig.edges(char0, char)=1
dig.edges?
dig.edges()
dig.edges.data()
dig.edges.data
dig.edges.data()

dig = nx.DiGraph()
for line in lines:
    char0 = ''
    for char in line:
        if dig.has_node(char):
            dig.node[char]['weight']+=1
        else:
            dig.add_node(char, weight=1)
        if char0=='':
            char0=char
        else:
            if False:#dig.has_edge(char0, char):
                pass #dig.edges(char0, char)+=1
            else:
                dig.edges(char0, char)=1

dig = nx.DiGraph()
for line in lines:
    char0 = ''
    for char in line:
        if dig.has_node(char):
            dig.node[char]['weight']+=1
        else:
            dig.add_node(char, weight=1)
        if char0=='':
            char0=char
        else:
            if False:#dig.has_edge(char0, char):
                pass #dig.edges(char0, char)+=1
            else:
                dig.edges(char0, char)=1
dig.add_edges_from([(1,2),(1,3),(1,3)])
dig.edges
dig.edges.data
dig.edges.data()
dig.edges.data([1,2])
dig.edges.data((1,2))
dig.edges.data()
dig.edges.data()[0]
dig.edges.data((1,2))
dig.edges.data((1,3))
dig.edges(1,2)
dig.edges((1,2))
dig.edges((1,2,None))
dig[1][2]
dig[1][3]
dig.add_edges_from([(1,2,1),(1,3,1),(1,3,2)])
dig.add_edges_from([(1,2)])
dig.add_edges_from([(1,2)],la)
G.add_edges_from([(3, 4), (1, 4)], label='WN2898')
dig.add_edges_from([(3, 4), (1, 4)], label='WN2898')
dig.add_edges_from([(3, 4), (1, 4)], label='WN2898')
dig
dig.edges
dig[3][4]
dig.add_edges_from([(3, 4), (1, 4)], weight='WN2898')
dig[3][4]
lines
for char in lines[0].strip():
    print(char)
dct = {}
k = []
for char in lines[0].strip():
    k.append(char)
    if len(k)==2:
        dct.get(k, 0)+=1
        k = []
    else:
        continue
    #print(char)
dct = {}
k = []
for char in lines[0].strip():
    k.append(char)
    if len(k)==2:
        default = dct.get(k, 0)
        dct[k] = default+1
        k = []
    else:
        continue
    #print(char)
dct = {}
k = ()
for char in lines[0].strip():
    k.append(char)
    if len(k)==2:
        default = dct.get(k, 0)
        dct[k] = default+1
        k = ()
    else:
        continue
    #print(char)
dct = {}
k = ()
for char in lines[0].strip():
    k.add(char)
    if len(k)==2:
        default = dct.get(k, 0)
        dct[k] = default+1
        k = ()
    else:
        continue
    #print(char)
dct = {}
k = []
for char in lines[0].strip():
    k.append(char)
    if len(k)==2:
        default = dct.get(k, 0)
        dct[tuple(k)] = default+1
        k = ()
    else:
        continue
    #print(char)
dct = {}
k = []
for char in lines[0].strip():
    k.append(char)
    if len(k)==2:
        default = dct.get(tuple(k), 0)
        dct[tuple(k)] = default+1
        k = ()
    else:
        continue
    #print(char)
dct = {}
k = []
for char in lines[0].strip():
    k.append(char)
    if len(k)==2:
        default = dct.get(tuple(k), 0)
        dct[tuple(k)] = default+1
        k = []
    else:
        continue
    #print(char)
dct
dct = {}
k = []
for line in lines:
  k = []
  for char in lines[0].strip():
    k.append(char)
    if len(k)==2:
        default = dct.get(tuple(k), 0)
        dct[tuple(k)] = default+1
        k = []
    else:
        continue
    #print(char)
dct
dct
dct = {}
k = []
for line in lines:
  k = []
  for char in line.strip():
    k.append(char)
    if len(k)==2:
        default = dct.get(tuple(k), 0)
        dct[tuple(k)] = default+1
        k = []
    else:
        continue
    #print(char)
dct
#for k in dct:
dig.add_edges_from?
for k in dct:
    dig.add_edges_from([k], weight=dct[k])
dig
dig.edges
dig.edges['昨日']
dig.edges['乡村']
dig.edges['乡镇']
dig
%store dig
%store dct
ls
dig.edges.data
dig.edges.dataview
dig.edges.dataview()
dig.edges.dataview?
dig.edges.data?
dig.edges.data(weight)
dig.edges.data('weight')
sorted(dig.edges.data('weight'))
i[-1] for i in dig.edges.data('weight')
[i[-1] for i in dig.edges.data('weight')]
sorted([i[-1] for i in dig.edges.data('weight')])
dig
dig.root_graph
dig.root_graph()
dig.pred
import matplotlib
import matplotlib.pyplot as plt
nx.draw(dig,
        pos = nx.random_layout(dig), # pos 指的是布局,主要有spring_layout,random_layout,circle_layout,shell_layout
        node_color = 'b',   # node_color指节点颜色,有rbykw,同理edge_color 
        edge_color = 'r',
        with_labels = True,  # with_labels指节点是否显示名字
        font_size =18,  # font_size表示字体大小,font_color表示字的颜色
        node_size =20)  # font_size表示字体大小,font_color表示字的颜色
plt.savefig("network.png")
nx.write_gexf(dig, 'network.gexf')  # gexf格式文件可以导入gephi中进行分析
plt.show()
dig.edges.data('weights')
dig.edges.data('weight')
weights = dig.edges.data('weight')
sorted(weights, key=lambda x: x[-1], reverse=True)
sorted(weights, key=lambda x: x[2], reverse=True)
weights[0]
weights
type(weights)
list(weights)
weights = list(dig.edges.data('weight'))
sorted(weights, key=lambda x: x[2], reverse=True)
weights[0]
weights[2]
weights[10]
weights[10][-1]
type(weights[10][-1])
weights[4]
weights[3]
weights = weights[3:]
sorted(weights, key=lambda x: x[2], reverse=True)
[i[2] for i in weights]
type([i[2] for i in weights])
[type(i[2]) for i in weights]
set([type(i[2]) for i in weights])
[type(i[2]) for i in weights]
for i in weights
for i in weights:
    if type(i)==str:
        print(i)
for i in weights:
    if type(i[2])==int:
        print(i)
for i in weights:
    if type(i[2])==str:
        print(i)
weights.remove((3,4,'WN2898'))
sorted(weights, key=lambda x: x[2], reverse=True)
SORT_WEIGHTS = sorted(weights, key=lambda x: x[2], reverse=True)
%store SORT_WEIGHTS
SORT_WEIGHTS
SORT_WEIGHTS[:3]
SORT_WEIGHTS[-3:]
dig.degree('市','场')
dig.degree('市')
dig.degree('场')
%logstate
%logstartart
%logstart
%hist -f history.py
