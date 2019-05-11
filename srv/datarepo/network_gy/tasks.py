#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
from celery import Celery

app = Celery()
app.config_from_object("celeryconfig")  # 指定配置文件

@app.task
def taskA(x,y):
    return x + y

@app.task
def taskB(x,y,z):
    return x + y + z

@app.task
def add(x,y):
    return x + y
"""

from celery import Celery
from kombu import Queue
import time
import sys
sys.path.append("/home/distdev/anaconda3/lib/python3.6/site-packages")
import jieba
import address_activaty
from address_activaty import address_activaty

app = Celery('tasks', backend='redis://127.0.0.1:6379/6')
app.config_from_object('celeryconfig')

class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        print("----%s is done" % task_id)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

@app.task(base=CallbackTask) 
def add(x, y):
    return x + y

@app.task(base=CallbackTask) 
def multiply(x,y):
    return x*y
 
@app.task(base=CallbackTask) 
def handle_num(line):
    return address_activaty.handle_num(line)

