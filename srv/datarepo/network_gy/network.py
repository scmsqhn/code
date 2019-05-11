ps -af
ls
ls -lrth
ps -af
import networkx as nx
nx
di = nx.DiGraph()
di.add_edge(1,2)
di.add_edge(2,3)
di
di.edge
di.add_edge(1,3)
di.edge
nx.shortest_paths(1,2)
nx.shortest_paths(di,(1,2))
nx.shortest_paths(di,1,2)
nx.shortest_paths?
nx.shortest_paths??
nx.shortest_paths?
nx.shortest_paths??
nx.shortest_paths?
nx.shortest_paths(1,2)
nx.shortest_paths?
nx.shortest_paths??
di.get_edge_data
di.get_edge_data(1,2)
nx.shortest_path(1,2)
nx.single_source_shortest_path(1,2)
nx.single_source_shortest_path?
nx.single_source_shortest_path(di,1,2)
nx.single_source_shortest_path(di,(1,2))
nx.single_source_shortest_path(di,1,2)
nx.single_source_shortest_path(di,1,3)
nx.single_source_shortest_path(di)
nx.single_source_shortest_path(di,1,2)
nx.single_source_shortest_path(di,2,3)
nx.single_source_shortest_path(di,2)
nx.single_source_shortest_path(di,3)
nx.single_source_shortest_path(di,1)
nx.shortest_path(di,1,2)
nx.shortest_path(di,1,3)
nx.shortest_path(di,1,4)
di.add_edge(1,4)
di.add_edge(2,4)
nx.shortest_path(di,3,4)
for i in nx.shortest_path(di,3,4):
    print(i)
nx.shortest_path(di,4,5)
nx.shortest_path(di,5,6)
nx.shortest_path(di,1,2)
nx.shortest_path(di,2,)
%hist -f worknet.py
wd="someone"
for i in range(len("someone")-1):
    di.add_edge(wd[i],wd[i+1])
di.edge
nx.shortest_path(di,'s','o')
nx.shortest_path(di,'s','m')
nx.shortest_path(di,'s','e')
%hist -f network.py
