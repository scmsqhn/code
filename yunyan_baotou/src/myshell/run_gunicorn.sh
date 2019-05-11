#'''
#
#-c CONFIG, --config=CONFIG
#指定一个配置文件（py文件）.
#
#
#-b BIND, --bind=BIND
#与指定socket进行绑定.
#
#
#-D, --daemon
#以守护进程形式来运行Gunicorn进程，其实就是将这个服务放到后台去运行。
#
#
#-w WORKERS, --workers=WORKERS
#工作进程的数量。上边提到gunicorn是一个pre-fork worker模式，就是指gunicorn启动的时候，在主进程中会预先fork出指定数量的worker进程在处理请求时，gunicorn依靠操作系统来提供负载均衡，通常推荐的worker数量是：(2 x $num_cores) + 1
#
#
#-k WORKERCLASS, --worker-class=WORKERCLASS
#工作进程类型. 包括 sync（默认）, eventlet, gevent, or tornado, gthread, gaiohttp.
#
#
#--backlog INT
#最大挂起的连接数.
#
#
#--chdir
#切换到指定的工作目录.
#
#
#--log-level LEVEL
#输出error log的颗粒度，有效的LEVEL有:
#debug
#info
#warning
#error
#critical
#
#--access-logfile FILE
#确认要写入Access log的文件FILE. '-' 表示输出到标准输出.
#
#--error-logfile FILE, --log-file FILE
#确认要写入Error log的文件FILE. '-' 表示输出到标准错误输出.
#
#
#'''
gunicorn --access-logfile ./access.log --error-logfile ./error.log --log-level debug -k sync -w 1  ../web/main_web:app
#gunicorn --access-logfile ./access.log --error-logfile ./error.log --log-level debug -k sync -w 1  ../web/main_web:app

