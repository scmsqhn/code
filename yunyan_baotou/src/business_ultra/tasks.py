#encoding=utf-8
import pdb
from celery import Celery,platforms
from celery.exceptions import SoftTimeLimitExceeded
platforms.C_FORCE_ROOT = True
import time
from time import sleep
import socket
import numpy as np
import sys
import os
sys.path.append(os.environ['YUNYAN'])
sys.path.append(os.environ['ROOT'])
sys.path.append(os.environ['WORKBENCH'])
import myconfig
import celeryconfig as celeryconfig
import myconfig as myconfig
import src.business_ultra as business_ultra
import src.function_ultra as function_ultra
from src.business_ultra import matchHandler
from src.business_ultra import splitHandler
from src.function_ultra.mylog import logger
from src.function_ultra.redis_helper import RedisHelper
r = RedisHelper()
'''
celery app
'''
app = Celery('tasks',
    backend ='redis://127.0.0.1:6379/0',
    broker = 'redis://127.0.0.1:6379/1'
)
import yunyan
from yunyan.src.business_ultra import splitHandler
#from yunyan.src.business_ultra import possegHandler
from yunyan.src.business_ultra import matchHandler
#from yunyan.src.business_ultra import wordMatchHandler
#from yunyan.src.business_ultra import tensorHandler

split_handler_instance = splitHandler.init()
#possegcut_handler_instance = possegHandler.init()
match_handler_instance = matchHandler.init()
#tensor_handler_instance = tensorHandler.init()
#word_match_handler_instance = wordMatchHandler.init()

@app.task(ignore_result=True)    #这个hello函数不需要返回有用信息，设置ignore_rsult可以忽略任务结果
def hello():
    print('Hello,Celery!')

@app.task(soft_time_limit=500)
def add(x,y):
    sleep(5)
    return x+y

@app.task(soft_time_limit=50)
def add(x, y):
    time.sleep(3) # similar time cost
    s = x + y
    print("host ip {}: x + y = {}".format(get_host_ip(),s))
    return s

'''
@app.task(soft_time_limit=50)
def word_match(code):
    print('word match start')
    sent = r.get(str(code))
    print('\n> 标准词过滤输入:', sent)
    word_match_handler_instance.data = sent.decode('utf-8')
    return 0
'''
'''

@app.task(soft_time_limit=50)
def posseg_cut(code):
    print('\n>开始处理拆分',code)
    sent = r.get(str(code))
    print('\n>开始处理拆分',sent)
    possegcut_handler_instance.data = sent.decode('utf-8')
    return 0
'''
@app.task(soft_time_limit=5)
def search(code):
    try:
        '''
        sent: input texts
        code: input work type
        return: result after handle
        '''
        print('\n>开始处理比对',code)
        sent = r.get(str(code))
        print('\n>开始处理比对',sent)
        match_handler_instance.data = sent.decode('utf-8')
        return 0
    except SoftTimeLimitExceeded:
      return 0

'''
@app.task(soft_time_limit=50)
def pred(code):
    try:
      print('split start')
      #time.sleep(1) # similar time cost
      #sent: input texts
      #code: input work type
      #return: result after handle
      sent = r.get(str(code))
      print('sent is ', sent)
      #if myconfig.INIT_READY == False:
      print('\n\n\n\n\npred sent',sent)
      #handler work from the code
      tensor_handler_instance.data = 3 #np.random.randint([1000,3]) #sent.decode('utf-8')
      #while (1):
      #    print(mHandler.flag)
      #    if mHandler.flag == int('1000',2) or mHandler.flag == int('0100',2):
      #        break
      #    pass
      #mHandler.flag = 0
      return 0
      #search_result = r.get('1')
      #split_result = r.get('2')
      #r.set(str(rescode), sent.decode('utf-8'))
      #return code
    except SoftTimeLimitExceeded:
      return 0
'''
@app.task(soft_time_limit=50)
def split(code):
    #sent: input texts
    #code: input work type
    #return: result after handle
    print('\n>开始处理拆分',code)
    sent = r.get(str(code))
    print('\n>开始处理拆分',sent)
    split_handler_instance.data = sent.decode('utf-8')
    return 0

def get_host_ip():
    """
    get the ip of localhost
    return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    pass #app.start()


