#!
import json
import pdb
import re
import sys
import pandas as pd

input_file = sys.argv[1]
target_file = input_file.split('.')[0]+'.json'

lines = open(input_file,"r").readlines()
dct = {}
item = {}
for line in lines:
    if 'NEXT' in line:
        dct[len(dct)] = item
        item = {}
        pass
    else:
        print(line)
        if not '\t' in line:
            k = line
            v = ''
            item[k] = v
            continue
        k,v = line.split('\t')
        k,v = re.sub("[ \n]","",k), re.sub("[ \n]","",v)
        item[k] = v
fl = open(target_file,'w+',encoding='utf-8')
json.dump(dct,fl)

df = pd.DataFrame(dct)
df.T.to_csv(sys.argv[2])
fl = open(target_file,'r',encoding='utf-8')
info = json.load(fl)
print(info)
