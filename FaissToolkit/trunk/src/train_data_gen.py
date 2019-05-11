#! -*-coding:utf-8-*-
# -*-coding:utf-8-*-
# -*- coding: utf-8 -*-

import jieba
import os
import sys
sys.path.append('.')
sys.path.append('..')

import train_ner_cn
import numpy as np
import traceback
import random
import json
import requests
import sys
import pdb

CURDIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(CURDIR)
sys.path.append(os.environ['ROOT'])
import mylogger
from mylogger import logger
import address_formula_release.src.reghelper as reghelper


def strQ2B(ustring):
    rstring = ""
    logger.debug(ustring)
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    logger.debug(ustring)
    logger.debug(rstring)
    return rstring


regHelperInstance = reghelper.RegHelper()


def __pred(line, ner):
    '''
    usr locale function to get
    '''
    sys.path.append(os.path.join(os.environ['ROOT'], 'guiyang_real_population_address/trunk'))
    line = strQ2B(line)
    line.strip()
    __line__ = line
    base_result = regHelperInstance.address_formula(line)

    json_result = {}
    json_result[line] = {'entities': []}
    line = __line__
    logger.debug(base_result)
    for item in base_result:
        if item=='' or item[0]=='':
            continue
        if item[1] == 'rw':
            continue
        if item[1] == 'sent':
            continue
        if not item[0] in line:
            continue
        try:
            json_result[line]['entities'].append( \
                tuple((line.index(item[0]), line.index(item[0]) + len(item[0]), item[1])))
        except:
            logger.debug('try catch')
            logger.debug(item)
            traceback.print_exc()
            #pdb.set_trace()
            continue
    return json_result


def pred(line, ner):
    '''
    usr locale function to get
    '''
    line = strQ2B(line)
    json_result = {}
    json_result[line] = {'entities': []}
    results = train_ner_cn.test([line], ner)
    for result in results:
        for item in result:
            try:
                value = item[0]
                key = item[1]
                json_result[line]['entities'].append(
                    tuple((line.index(value), line.index(value) + len(value), key)))
            except BaseException:
                traceback.print_exc()
                logger.debug(line)
                logger.debug(value)
    return json_result

def test(line):
    '''
    use url to get data
    '''
    line = strQ2B(line)
    json_result = {}
    url = "http://127.0.0.1:7943/split"
    # url = "http://addr.triplet.com.cn/split"
    # url="http://localhost:18888/guizhou/normalization/addr-norm"
    headers = {
        'content-type': 'application/json',
        "Accept": "application/json"}
    body = {
        'messageid': "12",
        'clientid': "13",
        'text': [line],
        'encrypt': 'false',
    }
    response = requests.post(url, data=json.dumps(body), headers=headers)
    json_result[line] = {'entities': []}
    for item in list(json.loads(response.text)['result'].items()):
        if item[1] == '' or item[0] == 'rw' or item[0] == 'sent':
            continue
        try:
            value = item[1]
            key = item[0]
            # logger.debug(line.index(value))
            # logger.debug(key, value)
            json_result[line]['entities'].append(
                tuple((line.index(value), line.index(value) + len(value), key)))
        except BaseException:
            traceback.print_exc()
            logger.debug(line)
            logger.debug(value)
    return json_result


def read_file_trans(fn):
    nlp = train_ner_cn.init_model_4_pred('../../../guiyang_real_population_address/trunk/models/ner')

    result = {}
    cont = ''
    with open(fn, 'rb') as g:
        cont = g.read().decode('utf-8')
    lines = cont.split('\n')
    np.random.shuffle(lines)
    cnt = 0
    for line in lines[:3000]:
        try:
            json_result = __pred(line, nlp)
            #json_result = test(line)
            #json_result = pred(line, nlp)
            logger.debug(json_result)
            k = tuple(json_result.items())[0][0]
            v = tuple(json_result.items())[0][1]
            result[k] = v
            logger.debug('最终保存样本是')
            logger.debug(k)
            logger.debug(v)
            cnt += 1
            if cnt % 100 == 0:
                logger.debug(cnt)
        except BaseException:
            traceback.print_exc()
            continue
    with open("./ner_train.json", 'w') as json_file:
        json.dump(result, json_file)
    return 0


def read_ner_train_data():
    model = {}  # 存放读取的数据
    with open("./ner_train.json", 'r') as json_file:
        model = json.load(json_file)
    return model


if __name__ == '__main__':
    read_file_trans('./train_source_address.txt')
    #read_ner_train_data()
