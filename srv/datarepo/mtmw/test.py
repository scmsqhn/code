from tasks import *

re1 = taskA.delay(10, 20)
print(re1.result)

re2 = taskB.delay(1, 2, 3)
print(re2.result)

re3 = add.delay(1, 2)
print(re3.status)
