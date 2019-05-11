#!
## author ultra chengdu
## 19-01-12

## 启动服务
使用 celery -A tasks worker -n 2 启动多worker 
尽可能将速度提升交给celery 而不要开多线程，仅为我们不能确定，多线程的并发有利于提升，而celery的worker是一个个独立的任务，先天就是并发的

## 启动客户端
python celery_test.py
使用 celery -A tasks worker -n 2 启动多worker 
尽可能将速度提升交给celery 而不要开多线程，仅为我们不能确定，多线程的并发有利于提升，而celery的worker是一个个独立的任务，先天就是并发的

## 加载功能模块
文件 myconfig.py
ATTACH_LST = []
ATTACH_LST.append('RegRuleViewer')
>> 功能模块实现在myHandler中,在配置文件，增加类名
>> 配置好，需要挂载的功能模块即可

## 卸载功能模块
myHandler.release('RegRuleViewer')
功能模块的实现，可以在其他文件，挂载，释放，在myHandler文件

## issue needed
1. 很多地方在阻塞和非阻塞之间有些犹豫，对于应用场景没有吃透
2. 模块init 与注册监听机制，有些不适配，过多的初始化，消耗资源，临时初始化，业务伺服有不足
3. 集成部署

## 重启docker 重启服务
cd $YUNYAN/src/business_ultra
sh ../myshell/run_docker.sh

# 安装操作==========================================
## 初始化docker
cd /data/yunyan_baotou/src/business_ultra
sh ../myshell/docker_build.sh

## 启动docker
cd /data/yunyan_baotou/src/business_ultra
sh ../myshell/run_docker.sh

# 测试操作==========================================
## 测试程序
cd /data/yunyan_baotou/src/test
pthon request.py
