"""
this is a address search function
it's contain sevral model including
ui handle the customer input
db handle the db save and read
tree tree toplogi
graph graph toplogi
query compare search query
we use sevral process to handle this
"""
from multiprocessing import Process
import os
import my_graph
import trie_tree

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

def init_trees():
    dict_tree = trie_tree.Trie()
    addr_tree = trie_tree.Trie()


def init():
    print("let us init models")
    #init_db()
    init_trees()
    init_graph()
    while(1):
        run_ui()

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
