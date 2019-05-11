import pdb
# import quandl
# import arctic
import os
import pandas as pd
from bert_serving.client import BertClient
import traceback
import time
from arctic import Arctic
import pymongo
# import pdb
import logging
from logging.handlers import RotatingFileHandler
import re
from mylogger import logger
import myconfig
# ===========================
# logger setting
# ===========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#  logger = logging.getLogger(__name__)
logger.info("Start print log")
logger.debug("Do something")
logger.warning("Something maybe fail.")
logger.info("Finish")

handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)


rHandler = RotatingFileHandler("log.txt", maxBytes=1 * 1024, backupCount=3)
rHandler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rHandler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(rHandler)
logger.addHandler(console)


def init():
    # Connect to Local MONGODB
    logger.info('init start')
    store = Arctic("192.168.1.64:27018")
    # Create the library - defaults to VersionStore
    store.initialize_library('bert2vec')
    # Access the library
    library = store['bert2vec']
    c = pymongo.MongoClient(host=myconfig.MONGO_HOST, port=myconfig.MONGO_PORT)
    db = c.bert2vec
    coll = db.guizhou
    # lib,conn,db,coll
    logger.info('init ok')
    return library, c, db, coll


def init_bert():
    logger.info('init bert')
    bc = BertClient(
        ip="192.168.1.64",
        show_server_config=True,
        timeout=1000,
        port=5555,
        port_out=5556)
    logger.info('init bert SUCC')
    return bc

# get a id to label the data
def genarate_mongo_id(part):
    # return str(int(time.time())) + str(hash(part))
    return str(hash(part))


# spacify search in mongo collection
def search_in_mongo(coll, filed_name, value):
    return list(coll.find({filed_name: value}))

#    bc, # bert_serving  client
#    library, # mongo library
#    c, # connection
#    db, # db
#    coll, # collections
#    PATH, # path
#    sent_or_chars='chars'# sentence or chars)
def insert_sent_into_mongo(
        bc,
        library,
        c,
        db,
        coll,
        sent_or_chars='chars',
        PATH='/data/guizhou_19042/glue_dir/NCA/'
    ):
    for _, _, filenames in os.walk(PATH):
        for filename in filenames:
            if r'\,' in filename:
                if not filename.split(r'\.')[1] in ['tsv', 'csv', 'txt']:
                    # if not filename in ['train.tsv','test.csv','eval.tsv']:
                    continue
        try:
            open(os.path.join(PATH, filename), 'r').read()
            logger.info('handler the file %s' % filename)
        except BaseException:
            traceback.print_exc()
            continue
        for line in open(os.path.join(PATH, filename), 'r').readlines():
            try:
                parts = re.split('[\t\r\n]', line)
                for part in parts:
                    if len(re.findall('[\u4e00-\u9fa5]', part)) > 0:
                        print("RIGHT " + line)
                        if sent_or_chars == 'sent':
                            part = [part]
                        else:
                            part = list(part)
                        sentvec = bc.encode(part)
                        sentvecid = genarate_mongo_id(part)
                        library.write(
                            sentvecid, sentvec, metadata={
                                'sentvecid': sentvecid})
                        json_cell = {
                            'id': sentvecid,
                            'sent': part,
                            'sentvec': sentvec,
                        }
                        print(coll.insert(json_cell))
                        logger.info('handler the sent %s' % part)
                        # pdb.set_trace()
            except BaseException:
                traceback.print_exc()
                print("WRONG " + line)


def encode(bc, sent, flag='list'):
    '''
    bert google module 编解码
    '''
    sentvec = -1
    if flag == 'list':
        sentvec = bc.encode(list(sent))
    elif flag == 'char':
        sentvec = bc.encode([sent])
    return sentvec


def get_all_from_guizhou(coll):
    allsamp = coll.find({})
    return allsamp


def get_one_from_guizhou(coll):
    allsamp = coll.find_one({})
    return allsamp


def get_all_arr(coll, library):
    allsample = get_all_from_guizhou()
    for line in allsample:
        print(line)
        #pdb.set_trace()
        sentvec = line['sentvec']
        sent = line['sent']
        my_array = library.read(sentvec).data
        meta = library.read(sentvec).metadata
        yield my_array, meta, sent


def test_get_one_from_guizhou(coll):
    logger.info(get_one_from_guizhou(coll))


def test_get_all_arr(coll, library):
    gen = get_all_arr(coll, library)
    logger.info(gen.__next__())

def read_csv_from_data():
    # read in all csv file in ~/data
    # file from guizhou, secret
    fetch_shape_size=100
    for i in range(1,9):
            fname = '/home/siy/data/%s.csv'%i
            fetch_shape=[]
            logger.info('read file %s.csv'%i)
            df = pd.read_csv(fname)
            df = df.astype('str')
            logger.info(str(df.head()))
            for col in df.columns:
                cells = df[col]
                for cell in cells:
                    cell = str(cell)
                    cell.strip()
                    cell = strQ2B(cell)
                    fetch_shape.append(cell)
                    if len(fetch_shape) > fetch_shape_size:
                        yield fetch_shape
                        # arrs_fetch = bc.encode(fetch_shape)
                        fetch_shape=[]
            #yield fetch_shape

#
def sents2vec(gen, coll, bc, library):
    '''
    read data from gen
    fetch vec from sent
    save date into mongo
    '''
    for sents in gen:
      print(sents)
      try:
          arrs = bc.encode(sents)
      except:
          print(sents)
          continue
      for sent,sentvec in zip(sents,arrs):
        sentvecid = genarate_mongo_id(sent)
        weather_sent_exist = search_in_mongo(coll, 'id', sentvecid)
        if not len(weather_sent_exist) == 0:
            logger.info('there is one in db: %s'%sent)
            continue
        library.write(sentvecid, sentvec, metadata={'sentvecid': sentvecid})
        json_cell = {'id': sentvecid, 'sent': sent}
        coll.insert(json_cell)
        logger.info('insert %s'%sent)




if __name__ == '__main__':
    lib, c, db, coll = init()
    bc = init_bert()
    gen = read_csv_from_data()
    sents2vec(gen, coll, bc, lib)
    #print(gen.__next__())
    #test_get_one_from_guizhou(coll)
    # test_get_all_arr(coll, lib)
