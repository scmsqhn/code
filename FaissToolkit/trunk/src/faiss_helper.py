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
