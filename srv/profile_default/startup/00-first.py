#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: 00-first.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-06
#   describe:
#================================================================

import os
import sys
import pandas as pd
import numpy as np
import tensorflow as tf
import pdb
from bert_serving.client import BertClient
import traceback
import time
from arctic import Arctic
import pymongo
import logging
from logging.handlers import RotatingFileHandler
import re

# 配置数据库
def init():
    # Connect to Local MONGODB
    #logger.info('init start')
    store = Arctic("192.168.1.64:27018")
    # Create the library - defaults to VersionStore
    store.initialize_library('bert2vec')
    # Access the library
    library = store['bert2vec']
    c = pymongo.MongoClient(host='192.168.1.64', port=27018)
    db = c.bert2vec
    coll = db.guizhou
    # lib,conn,db,coll
    #logger.info('init ok')
    print('init ok')
    return library, c, db, coll

arclib, client, db, coll = init()


