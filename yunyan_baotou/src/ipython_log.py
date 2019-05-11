# IPython log file


get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('pwd', '-P')
get_ipython().run_line_magic('cd', '~')
get_ipython().run_line_magic('cd', 'code/')
get_ipython().run_line_magic('cd', 'srv/')
get_ipython().run_line_magic('cd', 'yunyan_baotou/')
get_ipython().run_line_magic('ls', '')
dig
dig.nodes
len(dig.nodes)
nx.shortest_simple_paths
nx.shortest_simple_paths(dig, '北', '晶')
import networkx as nx
nx.shortest_simple_paths(dig, '北', '晶')
pts = nx.shortest_simple_paths(dig, '北', '晶')
len(pts)
list(pts)
pts.__next__()
pts = nx.shortest_simple_paths(dig, '北', '晶')
pts.__next__()
pts.__next__()
pts.__next__()
pts.__next__()
pts.__next__()
pts.__next__()
pts.__next__()
pts.__next__()
pts.__next__()
pts.__next__()
pts.__next__()
get_ipython().run_line_magic('pinfo', 'nx.shortest_path_length')
exit()
