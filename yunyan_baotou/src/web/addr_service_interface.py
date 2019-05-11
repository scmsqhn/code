#!/usr/bin/python
#coding:utf8
'''
Abstract Factory of webservice generate
'''

import threading
import pdb
import json
import flask
import random
import sys
#import singal
from flask import Flask, Response
import os
import myconfig
sys.path.append(os.environ['YUNYAN'])
sys.path.append(os.environ['WORKBENCH'])
print(sys.path)
from src.function_ultra import utils
from flask import Blueprint
from flask import Flask,url_for,redirect,render_template,request
from src.business_ultra.master import split as split
from src.business_ultra.master import search as search
from src.business_ultra.master import word_match as word_match
#from src.business_ultra.master import pred as pred
from src.business_ultra.master import posseg_cut as posseg_cut

class IbaResponse(Response):
    default_mimetype = 'application/json'

class IbaFlask(Flask):
    response_class = IbaResponse

class AddrServiceConfig(object):
    def __init__(self):
      self.name = 'service_name'
      self.child_sys_id = 'yunyan_address'
      self._id = -1
      self.host = '0.0.0.0'
      self.port= 7945
      self.baseurl = 'normalization'
      self.func_name = []

main=Blueprint('main',__name__)

def set_timeout(num, callback):
    def wrap(func):
        def handle(signum, frame):
            raise RuntimeError
        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)
                signal.alarm(num)
                print('start alarm signal.')
                r = func(*args, **kwargs)
                print('close alarm signal.')
                signal.alarm(0)
                return r
            except RuntimeError as e:
                callback()
        return to_do
    return wrap

def after_timeout():
    print("Time out!")

@main.route('/word-match', methods=['POST'])
def addr_match():
        '''address split split'''
        param = json.loads(flask.request.data.decode('utf-8'))
        text = param.get('text')
        predict_result = word_match(text)
        msgid = param.get('messageid')
        cltid = param.get('clientid')
        resultcode = '000'
        result = {
            'messageid': msgid,
            'clientid': cltid,
            'resultcode': '000',
            'result': predict_result,
        }
        return json.dumps(result)

@main.route('/split', methods=['POST'])
def addr_split():
        '''address split split'''
        print('\n> request 访问数据',flask.request.data)
        print('\n> request 访问数据',flask.request.data.decode('utf-8'))
        param = json.loads(flask.request.data.decode('utf-8'))
        text = param.get('text')
        predict_result = split(text)
        msgid = param.get('messageid')
        cltid = param.get('clientid')
        resultcode = '000'
        result = {
            'messageid': msgid,
            'clientid': cltid,
            'resultcode': '000',
            'result': predict_result,
        }
        print('\n> split',result)
        return json.dumps(result)

def set_timeout(num,callback):
  def wrap(func):
    def handle(signum, frame):
        raise RuntimeError

    def to_do(*args, **kwargs):
        try:
            signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
            signal.alarm(num)  # 设置 num 秒的闹钟
            print('start alarm signal.')
            r = func(*args, **kwargs)
            print('close alarm signal.')
            signal.alarm(0)  # 关闭闹钟
            return r
        except RuntimeError as e:
            callback()
    return to_do
  return wrap

def after_timeout():  # 超时后的处理函数
    print("Time out!")

'''
@main.route('/pred', methods=['POST'])
def addr_pred():
        #address search
        param = json.loads(flask.request.data.decode('utf-8'))
        text = param.get('text')
        predict_result = pred(text)
        msgid = param.get('messageid')
        cltid = param.get('clientid')
        result = {
            'messageid': msgid,
            'clientid': cltid,
            'resultcode': '000',
            'result': ' '.join(predict_result),
        }
        print('\n> pred ',result)
        return json.dumps(result)
'''

@main.route('/posseg-cut', methods=['POST'])
def addr_posseg_cut():
        param = json.loads(flask.request.data.decode('utf-8'))
        text = param.get('text')
        print('\n>possegcut url 输入',text)
        predict_result = posseg_cut(text)
        print('\n>possegcut predict result ',predict_result)
        msgid = param.get('messageid')
        cltid = param.get('clientid')
        result = {
            'messageid': msgid,
            'clientid': cltid,
            'resultcode': '000',
            'result': predict_result,
        }
        print('\n>posseg_cut 输出 url:',result)
        return json.dumps(result)

@main.route('/search', methods=['POST'])
def addr_search():
        '''address search'''
        param = json.loads(flask.request.data.decode('utf-8'))
        text = param.get('text')
        print(text)
        predict_result = search(text)
        print(predict_result)
        msgid = param.get('messageid')
        cltid = param.get('clientid')
        result = {
            'messageid': msgid,
            'clientid': cltid,
            'resultcode': '000',
            'result': ' '.join(predict_result),
        }
        print('\n> search',result)
        return json.dumps(result,ensure_ascii=True)

if __name__ == "__main__":
    pass
    from src.business_ultra.master import word_match as word_match
    predict_result = word_match('贵阳市云岩区北京西路')
    print(predict_result)

    #yunyan_service = AddrServiceInterface()
    #yunyan_service.run()

