#bin/bash
bashdir=/root/iba/dmp/gongan/gy_addr_normal
cd $bashdir
ls -l
nohup python word_vob_gen.py & >>$bashdir/word_vob_gen_log.txt

#cp $bash_dir/pre_data/*.* $bash_dir/data/

