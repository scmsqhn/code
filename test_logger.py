rHandler=RotatingFileHandler("log.txt",maxBytes=1000*1024,backupCount=3)
rHandler.setLevel(logging.INFO)
formatter=logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
rHandler.setFormatter(formatter)
console=logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(rHandler)
logger.addHandler(console)


logger.debug('debug')
logger.debug('debug2')
logger.debug('debug3')
