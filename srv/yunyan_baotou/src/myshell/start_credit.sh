#! /bin/bash
export PYTHONPATH=/usr/local/credit_daemon
export DMPPATH=/usr/local/credit_daemon
export PATH=/opt/conda/bin:$PATH
cd $DMPPATH/dap

while true;
do
  count=`ps -fe | grep "cbc_server" | grep -v "grep"`
  if [ "$?" != "0" ]; then
    nohup python cbc_server.py >> cbc.log 2>&1 &
  fi
  sleep 2
done