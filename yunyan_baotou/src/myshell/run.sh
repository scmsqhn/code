#!/bin/bash

export YUNYAN=/root/yunyan
export WORKBENCH=/root
export ROOT=/root
echo $YUNYAN
echo $WORKBENCH
echo $ROOT

ps -ef | grep 7946 | awk 'print {$2}' | xargs kill -9 
ps -ef | grep main_web.py | awk 'print {$2}' | xargs kill -9 
ps -ef | grep celery | awk 'print {$2}' | xargs kill -9 
cd /root/yunyan/
pip install -r requirments.txt

cd /root/yunyan/src/business_ultra 
echo 'cd /root/yunyan/src/business_ultra'

redis-server & 
echo 'redis-server &'

nohup celery -A tasks worker --loglevel=info -n 8 &1>2 &
echo 'nohup celery -A tasks worker --loglevel=info -n 1 &1>2 &'

python ../web/main_web.py
echo 'python ../web/main_web.py'
#nohup python ../web/main_web.py &1>2 & 

# front running
# celery -A tasks worker & # back running
# celery -A my_first_celery worker -l info
