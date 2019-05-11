# coding: utf-8
#!/usr/bin/env sh

export LD_LIBRARY_PATH=/opt/conda/lib:$LD_LIBRARY_PATH
export PATH=/opt/conda/bin:$PATH
export PYTHONPATH=$HOME/iba
export DMPPATH=$HOME/iba
cd $DMPPATH/bin

CONF_LIST="zz_wp_ner.conf
ner_victim_info.conf
comm_time_parse.conf"


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
