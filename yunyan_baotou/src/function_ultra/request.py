#/usr/bin/bash
#/coding = 'utf-8'

import numpy as np
import sys
import jieba
import os
sys.path.append('.')
sys.path.append('..')
import requests
import json
import random
import traceback
CURDIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(CURDIR)
#from db_inf import *
#import name_parse
#from name_parse.predict import  parse_name
#import word2vec
#from word2vec import _gensim_word2vec as word2vec
import json


def test(line):
    url="http://localhost:7943/normalization/addr-normal"
    #url="http://localhost:18888/guizhou/normalization/addr-norm"
    headers = {'content-type': 'application/json', "Accept": "application/json"}
    body = {
        'messageid': "12",
        'clientid': "13",
        'text':[line],
        'encrypt':'false',
        }
    response = requests.post(url, data = json.dumps(body), headers = headers)
    print(response.text)
    print(response.status_code)

if __name__ == '__main__':
    line = '黄山冲20号'
    test(line)
