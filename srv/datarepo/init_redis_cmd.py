#!
import os    
import re

def _init_redis():
      cnt = 0
      outfile = open("./redis_cmd_insert_data.txt","a+")
      stand_lines = open("./data/std/zz_std_words.txt","r").readlines()
      for line in stand_lines:
        line = re.sub("[\r\n]","",line)
        words = line.split(" ")
        for word in words:
          outfile.write("SADD %s %s\n"%(word,str(hash(line))))
        cnt+=1
        if cnt%100000 == 1:
          print(cnt)
      return 0

_init_redis()
