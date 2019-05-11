# coding: utf-8
#!/usr/bin/env sh

export LD_LIBRARY_PATH=/opt/conda/lib:$LD_LIBRARY_PATH
export PATH=/opt/conda/bin:$PATH
export PYTHONPATH=$HOME/iba
export DMPPATH=$HOME/iba
cd $DMPPATH/bin

CONF_LIST="bj_crim_110_classify.conf
bj_crim_110_loc.conf
bj_crim_110_ner.conf
bj_crim_loc_classify.conf
bj_crim_suspect_classify.conf
bj_crim_vehicle_classify.conf
comm_name_parse.conf
comm_time_parse.conf
gz_wp_ner.conf
sjz_period_time.conf
case_time.conf
bj_wyc_addr_norm_map.conf"


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
