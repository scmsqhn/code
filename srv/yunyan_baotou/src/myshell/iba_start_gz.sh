# coding: utf-8
#!/usr/bin/env sh

export LD_LIBRARY_PATH=/opt/conda/lib:$LD_LIBRARY_PATH
export PATH=/opt/conda/bin:$PATH
export PYTHONPATH=$HOME/iba
export DMPPATH=$HOME/iba
cd $DMPPATH/bin

"""

CONF_LIST=" gz_basic_case_classify.conf
addr_norm_trans.conf
comm_name_parse.conf
comm_time_parse.conf
comm_property_parse.conf
cbc_server.conf
gz_crim_loc_classify.conf
gz_crim_loc_ner.conf
gz_crim_method_classify.conf
gz_crim_phone_num.conf
gz_crim_type_classify.conf
gz_wp_ner.conf
gz_basic_case_classify.conf
gz_crim_loc_ner_test.conf"

"""
CONF_LIST="gz_address_formula.conf
gz_basic_case_classify.conf"


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
