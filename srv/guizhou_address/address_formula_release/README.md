
# 2019-01-03
# 实口拆分方案部署

# 命令
docker run -d --privileged=true --net=host -v /data/docker_iba/iba:/root/iba -e PYTHONIOENCODING=utf-8 -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 -e DMPPATH=/root/iba -e PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin -e PYTHONPATH=/root/iba --name shikou2019 split_server:haining/bin/bash /root/iba/bin/iba_start.sh

#sh ./myshell/check_every_day.sh
# 运行每日检验程序，结果在./pred/tmp.txt

#sh python json_file.py ./pred/tmp.txt 
# 运行文件更新程序，结果在target_file.csv

# 词库优化方式
修改 ./dct_file/dct_level 下的词库文件，讲对应级别的词放入相应文件
通过拆分接口发送命令 CMDDCT
词库秒级动态加载
结束
