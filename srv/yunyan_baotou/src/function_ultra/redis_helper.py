import sys
import os
import myconfig
import redis

class RedisHelper(object):
    def __init__(self):
        self.r = redis.Redis(host=myconfig.REDIS_HOST_DAT, port=myconfig.REDIS_HOST_DAT_PORT,db=1)

    def set(self,k,v):
        self.r.set(str(k), str(v))

    def get(self,k):
        #return self.r.get(self.bt(str(k),'sb'))
        #return self.r.get(str(k)).decode('utf-8')
        return self.r.get(str(k))

    def bt(self, b, direct='bs'):
        if direct == 'bs':
            return str(b, encoding = "utf8")
        else:
            return bytes(b, encoding = "utf8")

if __name__ == '__main__':
   r =  RedisHelper()
   r.set('1','来电')
   res = r.get('1')
   print(res)
