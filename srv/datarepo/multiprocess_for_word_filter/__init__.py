#!

"""使用celery 处理分布式任务，完成地址检索"""
from celery import Celery,platforms 
app = Celery('tasks',backend='amqp',broker='amqp://public:distdev@192.168.12.103:5672/') 
platforms.C_FORCE_ROOT = True 

@app.task
  def add(x,y): 
    return x + y
