#!/bin/bash
# enter docker 
# ssh root@192.168.1.4
# 123456
sudo docker run -p 18888:7943 -v /data/docker/iba:/root/iba --privileged=true -v /data/docker/nginx:/root/ngingx -it 4961e870065e /bin/bash

