#! /bin/bash
export PYTHONPATH=/usr/local/credit_daemon
export DMPPATH=/usr/local/credit_daemon
export PATH=/opt/conda/bin:$PATH
cd $DMPPATH/dap

count=`ps -fe | grep "machine_learning" | grep -v "grep"`
if [ "$?" != "0" ]; then
  nohup python machine_learning.py >> machine.log 2>&1 &
fi
