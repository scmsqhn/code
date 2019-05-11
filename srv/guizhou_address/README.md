
# 2019-01-03
# 实口拆分方案部署

# 命令
docker run -d --privileged=true --net=host -v /data/docker_iba/iba:/root/iba -e PYTHONIOENCODING=utf-8 -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 -e DMPPATH=/root/iba -e PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin -e PYTHONPATH=/root/iba --name shikou2019 split_server:haining/bin/bash /root/iba/bin/iba_start.sh

# address_formula_release 发布拆分版本
# address_match_release 发布比对版本

# src 全部源码

# python eval.py 黄山冲20号 拆分单条语测试

# sh ~/myshell/check_
