#!
import json

target_file = './standard_addr.json'
fl = open(target_file,'r',encoding='utf-8')
info = json.load(fl)
with open('stand_addr.txt','w') as g:
    g.write(str(info))
print(info)

