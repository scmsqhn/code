# coding: utf-8
#!/usr/bin/env sh

export LD_LIBRARY_PATH=/opt/conda/lib:$LD_LIBRARY_PATH
export PATH=/opt/conda/bin:$PATH
export PYTHONPATH=$HOME/iba
export DMPPATH=$HOME/iba
cd $DMPPATH/bin

CONF_LIST="sd_crim_110_classify.conf
sd_crim_110_ner.conf
bj_crim_110_ner.conf
comm_name_parse.conf
comm_time_parse.conf
gz_wp_ner.conf
cbc_server.conf
sdst_time_parse.conf
sdst_period_time.conf
sd_crim_chuzuwu_classify.conf
sd_crim_jiesuofangshi_classify.conf
sd_crim_jinrufangshi_classify.conf
sd_crim_kongjianbuwei_classify.conf
sd_crim_ruhudao_classify.conf
sd_crim_sheanchangsuo_classify.conf
sd_crim_zuoanshiji_classify.conf
sdst_wp_ner.conf"


for cfg in $CONF_LIST
do
    cfg_name=`basename $cfg`
    cfg_tag=${cfg_name%.*}
    count=`ps -fe | grep gunicorn | grep -w "$cfg_tag" | grep -v "grep"`
    if [ "$?" != "0" ]; then 
        echo "gunicorn -c cfg/$cfg dap.$cfg_tag:app --daemon"
        gunicorn -c cfg/$cfg dap.$cfg_tag:app --daemon
    fi
done

tail -f /dev/null
