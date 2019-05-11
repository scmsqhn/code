#!/bin/bash

ps -ef | grep 7746 | awk '{print $2}' | xargs kill -9 
ps -ef | grep 6379 | awk '{print $2}' | xargs kill -9 
ps -ef | grep main_web.py | awk '{print $2}' | xargs kill -9 
ps -ef | grep celery | awk '{print $2}' | xargs kill -9 
ps -ef | grep redis | awk '{print $2}' | xargs kill -9 

#export ROOT=/usr/local/lib/python3.6/site-packages
#export PYTHONPATH=/usr/local/lib/python3.6/site-packages
#export ROOT=/home/hn/anaconda3
#export YUNYAN=/home/hn/yunyan/yunyan_baotou
#echo -v $ROOT:/root
#echo -v $PRJ:/root/yunyan
#    --privileged=true --net=host -P \
#sudo docker remove myredis
#sudo docker run -d -P redis /bin/bash redis-server &
docker run \
    --name="baotou_address" \
    --privileged=true --net=host -P \
    --env ROOT:/root \
    --env WORKBENCH:/root \
    --env YUNYAN:/root/yunyan \
    -v /bin/bash:/bin/bash \
    -v /data/yunyan_baotou:/root/yunyan \
    -e PYTHONPATH=/root/anaconda3/bin \
    -e LANG=C.UTF-8 \
    -e LC_ALL=C.UTF-8 \
    -e PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin -it python:3.6 \
    /bin/bash

