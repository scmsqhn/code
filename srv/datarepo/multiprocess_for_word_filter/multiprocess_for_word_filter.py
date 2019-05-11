#!coding:utf-8
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support, Queue

# 任务个数
task_number = 10

# 收发队列
task_quue = Queue(task_number)
result_queue = Queue(task_number)


def get_task():
    return task_quue

def get_result():
    return result_queue

# 创建类似的queueManager
class QueueManager(BaseManager):
    pass

def win_run():
    # 注册在网络上，callable 关联了Queue 对象
    # 将Queue对象在网络中暴露
    #window下绑定调用接口不能直接使用lambda，所以只能先定义函数再绑定
    QueueManager.register('get_task_queue', callable=get_task)
    QueueManager.register('get_result_queue', callable=get_result)
    # 绑定端口和设置验证口令
    manager = QueueManager(address=('113.204.229.74', 15001), authkey='Unyur>okDot1'.encode())

    # 启动管理，监听信息通道
    manager.start()

    try:

        # 通过网络获取任务队列和结果队列
        task = manager.get_task_queue()
        result = manager.get_result_queue()

        # 添加任务
        for url in ["ImageUrl_" + str(i) for i in range(10)]:
            print('url is %s' % url)
            task.put(url)

        print('try get result')
        for i in range(10):
            print('result is %s' % result.get(timeout=10))

    except:
        print 'Manager error'
    finally:
        manager.shutdown()


if __name__ == '__main__':
    # window下多进程可能有问题，添加这句话缓解
    freeze_support()
    win_run()
