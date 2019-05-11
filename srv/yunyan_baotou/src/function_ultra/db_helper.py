#!
'''
database helper for all situation
19.01.09
qin hai ning
'''

import redis
import myconfig
class RdsInstance():
    def __init__(self):
        self.conn = self.init_redis()

    def init_redis(self):
        host = myconfig.RDSHOST
        port = myconfig.RDSPORT
        pool = redis.ConnectionPool(host=RDSHOST, port=RDSPORT)
        r = redis.Redis(connection_pool=pool)
        return r

    def cnt_req(r):
        r.setbit("uv_count1", 5,1)
        r.setbit("uv_count1", 8,1)
        r.setbit("uv_count1", 3,1)
        r.setbit("uv_count1", 3,1)
        print("uv_count:", r.bitcount("uv_count1"))
