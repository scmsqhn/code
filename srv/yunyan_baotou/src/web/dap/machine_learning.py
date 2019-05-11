# coding=utf-8
from dmp.algor.machine_learning import ML
from dutil.log import logger

ml = ML()
while True:
    if ml.get_task():
        logger.debug('begin machine learning')
        ml.load_data()
        ml.execute_modle_fit()
        logger.debug('end machine learning')
