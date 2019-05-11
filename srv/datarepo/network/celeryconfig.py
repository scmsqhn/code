#!/usr/bin/env python
#-*- coding:utf-8 -*-

from kombu import Exchange,Queue

#BROKER_URL = "redis://:your_password@127.0.0.1:6379/1"
#CELERY_RESULT_BACKEND = "redis://:your_password@127.0.0.1:6379/1"
BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'amqp://'

CELERY_QUEUES = (
    Queue("default",Exchange("default"),routing_key="default"),
    Queue("for_task_A",Exchange("for_task_A"),routing_key="for_task_A"),
    Queue("for_task_B",Exchange("for_task_B"),routing_key="for_task_B")

)
# 路由
CELERY_ROUTES = {
    'tasks.taskA':{"queue":"for_task_A","routing_key":"for_task_A"},
    'tasks.taskB':{"queue":"for_task_B","routing_key":"for_task_B"}

}
CELERY_DEFAULT_QUEUE = 'default'   # 设置默认的路由
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'

CELERY_TASK_RESULT_EXPIRES = 10  # 设置存储的过期时间　防止占用内存过多
