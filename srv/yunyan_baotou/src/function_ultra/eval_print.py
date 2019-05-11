#!
import json

target_file = 'eval_file_1228.json'
fl = open(target_file,'r',encoding='utf-8')
info = json.load(fl)
print(info)

