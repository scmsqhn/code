#!

'''
this is master file to handle all business jobs
import func add from file task.py
'''

'''
rsync call
'''
import time
from tasks import add
import function_ultra
r = function_ultra.redis_helper.RedisHelper()

result = add.delay(23,1)
print(result)
while not result.ready():
   print(time.strftime("%H:%M:%S"))
print(result)
print(result.get())
print(result.successful())

