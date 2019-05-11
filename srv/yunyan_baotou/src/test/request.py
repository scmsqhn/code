#/usr/bin/bash
#/coding = 'utf-8'
import re
import pdb
import os
import sys
import time
sys.path.append('../..')
import myconfig
sys.path.append(os.environ['YUNYAN'])
sys.path.append(os.environ['WORKBENCH'])
import sys
import os
import requests
import json
import random
import traceback
CURDIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(CURDIR)
import json

#IP="localhost"
IP="58.17.133.80"
url_1="http://%s:15005/normalization/split"%IP
url_2="http://%s:15005/normalization/search"%IP
url_3="http://%s:15005/normalization/word-match"%IP
#url_4="http://83.103.1.14:15005/normalization/pred"
url_5="http://%s:15005/normalization/posseg-cut"%IP

def test(line,url):
    print('url, line')
    print(url, line)
    headers = {'content-type': 'application/json', "Accept": "application/json"}
    body = {
        'messageid': "12",
        'clientid': "13",
        'text':line,
        'encrypt':'false',
        }
    print('\n> 访问url', url)
    print('\n> 访问body', body)
    response = requests.post(url, data = json.dumps(body), headers = headers)
    print('\n> response 返回', response)
    print('\n> response.text: ',response.text)
    print(response.text)
    return json.loads(response.text)

def check(src,g,url):
    kv = test(src,url)
    print('\n> url %s\n>src %s\n>kv %s'%(url,src,kv))
    return kv['result']

import function_ultra
from function_ultra import network_app
# 用于测试进行文本检查

def check_from_file(filename="./测试用例.txt",filename_out='./测试结果.txt'):
    g= open(filename_out, 'w+')
    lines = open(filename,'r').readlines()
    for line in lines:
        line.strip()
        if not '青山区' in line:
            continue
        print('line',line)
        step1 = check(line,g,url_1)
        print('step1',step1)
        #m_networkx_app = network_app.networkx_app()
        #step2 = m_networkx_app.search(step1)
        step2 = check(step1,g,url_2)
        step2 = re.sub("([^ ]) ","\\1",str(step2))
        print('step2',step2)
        g.write("%s\n"%(line))
        g.write("%s\n"%(str(step1)))
        for _step2_ in step2.split(','):
            g.write("%s\n"%(str(_step2_)))
        g.write("%s\n\n"%('===============\n'))
        g.flush()
    g.close()

if __name__ == '__main__':
    if True:
        check_from_file(filename="./测试用例.txt",filename_out='./测试结果.txt')
    else:
        line = '内蒙古包头市青山区'
        line2 = '内蒙古/PROV 包头市/DIST'
        g = open('tmp.txt','a')
        print('step1',check(line,g,url_1))
        print('step2',check(line2,g,url_2))


