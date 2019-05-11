#!/bin/bash
cd /data/nlppipeline
python /data/nlppipeline/filter_adabooster_addr.py
cp /data/nlppipeline/classifier.model /data/address_gy/
echo 'SUCC!'
