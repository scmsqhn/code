源文件服务器：192.168.1.4   root/123456    文件目录：/data/docker/iba/

========================================1.创建宿主机映射目录======================================================
1.1 压缩文件
压缩192.168.1.4上的iba项目成　/data/src/iba.tar.gz　,并将其拷贝到正式服务器/data/src
进入到192.168.1.4/data/src目录下执行如下操作
tar -czvf iba.tar.gz  /data/src
1.2 拷贝docker源文件到目标服务器
在目标服务器创建/data/src目录（root用户）
mkdir -p /data/src（作为宿主机根目录同时为项目的根目录，并把昨晚压缩的iba复制过来）

1.3上传docker镜像文件到目标服务器
镜像文件目录：192.168.1.4 服务器上 /data/src     镜像文件名称 iba_server.tar.gz

上传文件到目标服务器

特殊情况－－－－－centos７需要的权限：--privileged=true在第４步创建容器时执行，为项目开启特权　　参考博客－－－https://www.linuxidc.com/Linux/2015-03/115124.htm


========================================2.导入制作好的镜像文件======================================================
在目标服务器上执行如下操作，生成docker镜像
gunzip iba_server.tar.gz && cat iba_server.tar | sudo docker import - zhujian_server:yunyanqu

说明：
zhujian_server:yunyanqu　镜像名：（镜像tag）

查看导入进来的镜像文件,找到是否有自己创建的镜像(name和tag)：docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
iba_server2         new_tf1.6           6e191766b064        2 days ago          4.49 GB
zhujian_server      yunyanqu               ef5c22d1fe8b        3 days ago          4.49 GB
<none>              <none>              4961e870065e        3 months ago        4.49 GB


========================================3.创建容器======================================================
在目标服务器上执行如下操作，创建Python环境的docker容器

创建容器：docker run -d --privileged=true --net=host -v /data/src/iba:/root/iba -e PYTHONIOENCODING=utf-8 -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 -e DMPPATH=/root/iba -e PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin -e PYTHONPATH=/root/iba --name zhujian_server zhujian_server:yunyanqu /bin/bash /root/iba/bin/iba_start.sh

2019地址服务创建容器:
sudo docker run -p 18888:7943 -d --privileged=true --net=host -v /data/docker/src:/root/iba -e PYTHONIOENCODING=utf-8 -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 -e DMPPATH=/root/iba -e PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin -e PYTHONPATH=/root/iba --name address_server iba_server2:new_tf1.6/bin/bash /root/iba/bin/iba_start_gz.sh

2019地址服务创建容器:
sudo docker run -p 18888:7943 -d --privileged=true --net=host -v /data/docker/src:/root/iba -v /data/docker/nginx:/root/nginx -e PYTHONIOENCODING=utf-8 -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 -e DMPPATH=/root/iba -e PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin -e PYTHONPATH=/root/iba --name address_server3 iba_server2:new_tf1.6 /bin/bash /root/iba/bin/iba_start_gz.sh


说明：
/data/src/iba：宿主机的/data/src/iba目录
--privileged=true：centos7以上必须使用,开启特权
/root/iba:映射到容器的/root/iba
--name zhujian_server:（容器名）
zhujian_server:yunyanqu　（之前导入的镜像名）

查看已创建的容器列表:docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                     NAMES
a18072ff0c26        4961e870065e        "/bin/bash"              23 hours ago        Up 22 hours         0.0.0.0:18888->7943/tcp   wizardly_heyrovsky
d8e11a9d4a94        zhujian_server:yunyanqu   "/bin/bash /root/i..."   3 days ago    Up 22 hours                                   zhujian_server



========================================4.检查容器是否能正常工作======================================================
进入容器里面　：                         docker exec -it zhujian_server /bin/bash
启动./iba_sboot --project Yunyanqu ：  sudo docker exec -it zhujian_server /bin/bash -c "python /root/iba/bin/iba_sboot --project yunyanqu"
查看容器状态：                          sudo docker exec -it zhujian_server /bin/bash -c "python /root/iba/bin/iba_note --project yunyanqu"
重启容器：sudo docker restart zhujian_server

用110text.py或者curl命令测试是否正常返回数据
curl --request POST \
  --url http://192.168.1.4:11018/algor/zjaddrnormal \
  --header 'Content-Type: application/json' \
  --data '{"messageid": "111111111", "clientid": "22222", "encrypt": "false", "text": "云岩区东山路219号中天世纪新城七组团一期A3栋"}'


========================================其他命令========================================================
查看日志                               docker logs zhujian_server
Docker 引擎日志 ：   					　journalctl -u docker.service
重启docker服务：　　　　　　　　　　　　　　sudo service docker restart
停电启动docker：　　　　　　　　　　　　　　systemctl start docker




=================================docker环境新增依赖的包：以psycopg2-2.7.6.1-cp36-cp36m-manylinux1_x86_64.whl为例=================================
distdev@Spark03:~$ ll -rt *whl
-rw-r--r-- 1 distdev distdev 2678593 11月 12 15:30 psycopg2-2.7.6.1-cp36-cp36m-manylinux1_x86_64.whl


distdev@Spark03:~$ sudo docker cp psycopg2-2.7.6.1-cp36-cp36m-manylinux1_x86_64.whl zhujian_server:/root
distdev@Spark03:~$ sudo docker exec -it zhujian_server /bin/bash -c "pip install /root/psy*.whl"




======================================================报错：=====================================================================
rpc error: code = 2 desc = oci runtime error: exec failed: container_linux.go:247: starting container process caused "process_linux.go:75: starting setns process caused \"fork/exec /proc/self/exe: no such file or directory\""　重启docker服务即可解决
