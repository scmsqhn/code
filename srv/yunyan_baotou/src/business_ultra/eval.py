#!
import sys
import re
import reghelper
import pdb
regHelperInstance = reghelper.RegHelper('dummy')
f = sys.argv[1]
lines = [f]
#lines = open(f,'r').readlines()
#cnt = 10
for line in lines:
    result = regHelperInstance.address_formula(re.sub(" ","",line))
    print(line, '\n', result)
    #cnt-=1
    #if cnt<0:
    #    pdb.set_trace()


