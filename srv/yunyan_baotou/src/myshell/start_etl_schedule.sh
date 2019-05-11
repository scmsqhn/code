#! /bin/bash
#export PYTHONPATH=/home/hadoop/src
#export DMPPATH=/home/hadoop/src
#export PATH=/usr/bin:$PATH
#cd $DMPPATH/dmp/preYSprice

count=`ps -fe | grep "schedule_preprice.py" | grep -v "grep" |wc -l`
if [ "$count" = 0 ]; then
    #nohup python schedule_preprice.py >> preprice.log 2>&1 &
    python /home/hadoop/src/dmp/preYSprice/preprice.py >>/home/hadoop/src/bin/preprice.log  2>&1 &
else
  echo `date`: "schedule_preprice.py is alive"
fi
sleep 2
