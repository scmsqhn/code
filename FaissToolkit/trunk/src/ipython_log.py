# IPython log file


get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', '~/code')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', 'word_discover/')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', '..')
get_ipython().run_line_magic('cd', 'FaissToolkit/')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', 'trunk/')
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', 'src/')
get_ipython().run_line_magic('ls', '')
import bert2vec
get_ipython().run_line_magic('ls', '')
from bert2vec import *
get_ipython().run_line_magic('ls', '')
bert2vec.py
bert2vec
from bert2vec import *
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('pwd', '')
import src
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', '..')
get_ipython().run_line_magic('ls', '')
import src
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('cd', 'src/')
get_ipython().run_line_magic('ls', '')
from . import faiss_helper
from src. import faiss_helper
from src import faiss_helper
get_ipython().run_line_magic('ls', '')
get_ipython().run_line_magic('load', 'faiss_helper.py')
# %load faiss_helper.py
#!
# ================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: faiss_helper.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-04-26
#   describe:

import faiss                   # make faiss available
from mylogger import logger
# import bert2vec_read
from bert2vec_read import *
from bert2vec import init
from bert2vec import m2
import pymongo

def init_index(xb, d=768):
    index = faiss.IndexFlatL2(d)   # build the index
    print(index.is_trained)
    index.add(xb)                  # add vectors to the index
    print(index.ntotal)
    logger.info('faiss index init ok')
    return index


def search(index, xq, k=4, ll=5):
    D, Ins = index.search(xq, k)     # actual search
    print(I[:ll])                   # neighbors of the 5 first queries
    print(D[-ll:])                  # neighbors of the 5 last queries
    return D, I

def train_data_generator():
    lib, client, db, coll = bert2vec.init()
    results = coll.find({})
    for result in results:
        item = lib.read(result)
        yield item

def readSentFromMongo(sent, coll, library):
        lib.read(m2(line.encpde('utf-8')))
    return library, client, db, coll

if __name__ == "__main__":
    gen = train_data_generator()
    xb = []
    xbname = []
    for i in gen():
        xb.append(i.data)
        xbname.append(tuple(i.metadata.items())[1])
    index = init_index(xb)
    D, Ins = search(index, xq)
get_ipython().run_line_magic('load', 'faiss_helper.py')
# %load faiss_helper.py
#!
# ================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: faiss_helper.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-04-26
#   describe:

import faiss                   # make faiss available
from mylogger import logger
# import bert2vec_read
from bert2vec_read import *
from bert2vec import init
from bert2vec import m2
import pymongo

def init_index(xb, d=768):
    index = faiss.IndexFlatL2(d)   # build the index
    print(index.is_trained)
    index.add(xb)                  # add vectors to the index
    print(index.ntotal)
    logger.info('faiss index init ok')
    return index


def search(index, xq, k=4, ll=5):
    D, Ins = index.search(xq, k)     # actual search
    print(I[:ll])                   # neighbors of the 5 first queries
    print(D[-ll:])                  # neighbors of the 5 last queries
    return D, I

def train_data_generator():
    lib, client, db, coll = bert2vec.init()
    results = coll.find({})
    for result in results:
        item = lib.read(result)
        yield item

def readSentFromMongo(sent, coll, library):
        lib.read(m2(line.encpde('utf-8')))
    return library, client, db, coll

if __name__ == "__main__":
    gen = train_data_generator()
    xb = []
    xbname = []
    for i in gen():
        xb.append(i.data)
        xbname.append(tuple(i.metadata.items())[1])
    index = init_index(xb)
    D, Ins = search(index, xq)
# %load faiss_helper.py
#!
# ================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: faiss_helper.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-04-26
#   describe:

import faiss                   # make faiss available
from mylogger import logger
# import bert2vec_read
from bert2vec_read import *
from bert2vec import init
from bert2vec import m2
import pymongo

def init_index(xb, d=768):
    index = faiss.IndexFlatL2(d)   # build the index
    print(index.is_trained)
    index.add(xb)                  # add vectors to the index
    print(index.ntotal)
    logger.info('faiss index init ok')
    return index


def search(index, xq, k=4, ll=5):
    D, Ins = index.search(xq, k)     # actual search
    print(I[:ll])                   # neighbors of the 5 first queries
    print(D[-ll:])                  # neighbors of the 5 last queries
    return D, I

def train_data_generator():
    lib, client, db, coll = bert2vec.init()
    results = coll.find({})
    for result in results:
        item = lib.read(result)
        yield item

#def readSentFromMongo(sent, coll, library):
#        lib.read(m2(line.encpde('utf-8')))
#    return library, client, db, coll

if __name__ == "__main__":
    gen = train_data_generator()
    xb = []
    xbname = []
    for i in gen():
        xb.append(i.data)
        xbname.append(tuple(i.metadata.items())[1])
    index = init_index(xb)
    D, Ins = search(index, xq)

    
import faiss
get_ipython().system('pip install faiss_helper.py')
get_ipython().system('pip install fais')
get_ipython().system('pip install faiss')
get_ipython().run_line_magic('pip', 'install --upgrade pip')
get_ipython().system('pip install --upgrade pip')
get_ipython().run_line_magic('pip', 'install --upgrade pip')
get_ipython().system('pip install faiss')
# %load faiss_helper.py
#!
# ================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: faiss_helper.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-04-26
#   describe:

import faiss                   # make faiss available
from mylogger import logger
# import bert2vec_read
from bert2vec_read import *
from bert2vec import init
from bert2vec import m2
import pymongo

def init_index(xb, d=768):
    index = faiss.IndexFlatL2(d)   # build the index
    print(index.is_trained)
    index.add(xb)                  # add vectors to the index
    print(index.ntotal)
    logger.info('faiss index init ok')
    return index


def search(index, xq, k=4, ll=5):
    D, Ins = index.search(xq, k)     # actual search
    print(I[:ll])                   # neighbors of the 5 first queries
    print(D[-ll:])                  # neighbors of the 5 last queries
    return D, I

def train_data_generator():
    lib, client, db, coll = bert2vec.init()
    results = coll.find({})
    for result in results:
        item = lib.read(result)
        yield item

#def readSentFromMongo(sent, coll, library):
#        lib.read(m2(line.encpde('utf-8')))
#    return library, client, db, coll

if __name__ == "__main__":
    gen = train_data_generator()
    xb = []
    xbname = []
    for i in gen():
        xb.append(i.data)
        xbname.append(tuple(i.metadata.items())[1])
    index = init_index(xb)
    D, Ins = search(index, xq)

    
get_ipython().system('pip3 install faiss')
# %load faiss_helper.py
#!
# ================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: faiss_helper.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-04-26
#   describe:

import faiss                   # make faiss available
from mylogger import logger
# import bert2vec_read
from bert2vec_read import *
from bert2vec import init
from bert2vec import m2
import pymongo

def init_index(xb, d=768):
    index = faiss.IndexFlatL2(d)   # build the index
    print(index.is_trained)
    index.add(xb)                  # add vectors to the index
    print(index.ntotal)
    logger.info('faiss index init ok')
    return index


def search(index, xq, k=4, ll=5):
    D, Ins = index.search(xq, k)     # actual search
    print(I[:ll])                   # neighbors of the 5 first queries
    print(D[-ll:])                  # neighbors of the 5 last queries
    return D, I

def train_data_generator():
    lib, client, db, coll = bert2vec.init()
    results = coll.find({})
    for result in results:
        item = lib.read(result)
        yield item

#def readSentFromMongo(sent, coll, library):
#        lib.read(m2(line.encpde('utf-8')))
#    return library, client, db, coll

if __name__ == "__main__":
    gen = train_data_generator()
    xb = []
    xbname = []
    for i in gen():
        xb.append(i.data)
        xbname.append(tuple(i.metadata.items())[1])
    index = init_index(xb)
    D, Ins = search(index, xq)

    
conda
ps -af
get_ipython().run_line_magic('ls', '')
exit()
