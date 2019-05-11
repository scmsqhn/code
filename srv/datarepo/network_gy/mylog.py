import logging 

logger = logging.getLogger() 
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler() 
consoleHandler.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler('log.log', mode='w', encoding='UTF-8') 
fileHandler.setLevel(logging.NOTSET)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
consoleHandler.setFormatter(formatter) 
fileHandler.setFormatter(formatter)

logger.addHandler(consoleHandler) 
logger.addHandler(fileHandler)

logger.debug('debug 信息') 
logger.info('info 信息') 
logger.warning('warn 信息') 
logger.error('error 信息') 
logger.critical('critical 信息') 
logger.debug('%s 是自定义信息' % '这些东西')

