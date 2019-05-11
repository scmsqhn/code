#!/usr/bin/python
#coding:utf8

'''
Observer
'''
import sys
sys.path.append('..')
import business_ultra
from business_ultra.reghelper import RegHelper
from business_ultra.activity_match import ActiMatch
from function_ultra.redis_helper import RedisHelper

import myconfig
import yunyan
import pdb

r = RedisHelper()
mActiMatch = ActiMatch('dummy')

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

class AddrMatch(object):
    def update(self, subject):
        rescode = myconfig.SEARCH_RES
        code = subject.data
        print('search',code)
        res = mActiMatch.search(code)
        r.set(rescode,str(res))
        print('addrmatch',res)
        print('AddrMatch: update %s'%subject)
        print('AddrMatch: res %s'%res)
        subject.flag=int('1000',2)
        print(subject.flag)

# Example usage...
def init():
    '''
    attach the class from config attach_lst
    '''
    data1 = Data('Data 3')
    mAddrMatch = AddrMatch()
    data1.attach(mAddrMatch)
    return data1

def release(data1):
    '''
    deattach all module
    '''
    try:
        for key in myconfig.SEARCH_LST:
            view = myconfig.SEARCH_LST[key]()
            data1.detach(view)
    except:
        raise Exception("release wrong error!")

if __name__ == '__main__':
    pass#main()

