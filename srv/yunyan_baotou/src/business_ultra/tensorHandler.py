#!/usr/bin/python
#coding:utf8

'''
Observer
'''
import sys
import os
sys.path.append(os.environ['YUNYAN'])
sys.path.append(os.environ['WORKBENCH'])
import myconfig
import yunyan
#from yunyan.src.business_ultra.
from yunyan.src.business_ultra.reghelper import RegHelper
import business_ultra
from business_ultra.reghelper import RegHelper
from business_ultra.activity_match import ActiMatch
from function_ultra.redis_helper import RedisHelper
from business_ultra.multi_linear_classify_tens import sess_pred
import myconfig
import pdb
import numpy as np
r = RedisHelper()

class Handler(object):
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)

# Example usage
class Data(Handler):
    def __init__(self, name=''):
        Handler.__init__(self)
        self.name = name
        self._data = 0
        self.flag = 0

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.notify()

class DeepLearningViewer(object):
    def update(self, subject):
        #print(('HexViewer: Handler %s has data 0x%x' %
        #      (subject.name, subject.data)))
        print('DeepLearningViewer: update %s'%subject)
        r.set(subject.data)

class MachineLearnViewer(object):
    def update(self, subject):
        #print(('HexViewer: Handler %s has data 0x%x' %
        #      (subject.name, subject.data)))
        #subject.result.append('ml')
        print('MachineLearnViewer: update %s'%subject)

class TensorPredViewer(object):
    def update(self, subject):
        rescode = myconfig.PRED_RES
        code = subject.data
        res = sess_pred()
        print(rescode,res)
        r.set(rescode,res)
        subject.flag=int('0110',3)

# Example usage...
def init():
    '''
    attach the class from config attach_lst
    '''
    data1 = Data('Data 1')
    mTensorPredViewer = TensorPredViewer()
    data1.attach(mTensorPredViewer)
    return data1

def release(data1):
    '''
    deattach all module
    '''
    try:
        for key in myconfig.SPLIT_LST:
            view = myconfig.SPLIT_LST[key]()
            data1.detach(view)
    except:
        raise Exception("release wrong error!")

if __name__ == '__main__':
    pass#main()

