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
import network
import utils
import networkx as nx
from address_activity import address_activity

app = Celery('tasks', backend='amqp://guest@localhost//')
app.config_from_object('celeryconfig')

""""
class CallbackTask(task):
    def on_success(address_activity, retval, task_id, args, kwargs):
        print("----%s is done" % task_id)

    def on_failure(address_activity, exc, task_id, args, kwargs, einfo):
        pass
"""

@app.task()
def add(x, y):
    return x + y

@app.task()
def multiply(x,y):
    return x*y

@app.task()
def handle_text(line):
    """celery -A tasks worker -Q handle_text --concurrency=4 -l info -E -n worker1@%h"""
    line = utils.clr(str(line))
    line_pre = utils.before_first_num(line)
    res = address_activity.word_filter(line_pre)
    comm_nbs = []
    for i in range(len(res)-2):
        print(res)
        try:
            comm_nbs.append(list(nx.common_neighbors(address_activity.graph.di,res[i],res[i+1])))
        except:
            print("networkx error")
            continue
        comm_nbs.append(list(nx.common_neighbors(address_activity.graph.di,res[i],res[i+1])))
    result = address_activity.common_nbs(comm_nbs)
    return result,res


