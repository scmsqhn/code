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


if __name__ == "__main__":
    index = init_index(xb)
    D, Ins = search(index, xq)
