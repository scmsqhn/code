#!/bin/bash

python reghelper.py -r eval
> wrong_result.txt
> result_total.txt
python reghelper.py -r TEST
find ./result_total.txt | xargs grep ".*'rw': '1',.*"  > wrong_result.txt
more wrong_result.txt
