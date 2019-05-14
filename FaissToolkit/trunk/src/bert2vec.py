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
import hashlib
import sys


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


def init_md5():
    m2 = hashlib.md5()
    return m2


m2 = init_md5()


def strQ2B(ustring):
      """全角转半角"""
      rstring = ""
      for uchar in ustring:
          inside_code = ord(uchar)
          if inside_code == 12288:  # 全角空格直接转换
              inside_code = 32
          elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
              inside_code -= 65248
          rstring += chr(inside_code)
      return rstring


def init():
    # Connect to Local MONGODB
    logger.info('init start')
    store = Arctic("192.168.1.64:27018")
    # Create the library - defaults to VersionStore
    store.initialize_library('bert2vec')
    # Access the library
    library = store['bert2vec']
    client = pymongo.MongoClient(host=myconfig.MONGO_HOST, port=myconfig.MONGO_PORT)
    pdb.set_trace()
    db = client.bert2vec
    coll = db.guizhou
    # lib,conn,db,coll
    logger.info('init ok')
    return library, client, db, coll


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
def genarate_mongo_id(src):
    # return str(int(time.time())) + str(hash(part))
    #return str(hash(part))
    m2.update(src.encode())
    print(m2.hexdigest())
    return m2.hexdigest()


# spacify search in mongo collection
def search_in_mongo(coll, filed_name, value):
    try:
        return list(coll.find({filed_name: value}))
    except:
        logger.info('mongodb has no interdace here')
        return -2

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
                        #pdb.set_trace()
                        yield fetch_shape
                        # arrs_fetch = bc.encode(fetch_shape)
                        fetch_shape=[]
            #yield fetch_shape


def append_one(sent, coll, library, bc):
        print(sent)
        sentvecid = genarate_mongo_id(sent)
        weather_sent_exist = search_in_mongo(coll, 'id', sentvecid)
        if not len(weather_sent_exist) == 0:
            logger.info('there is one in db: %s'%sent)
            return -2
        sentvec = bc.encode([sent])
        #pdb.set_trace()
        library.write(sentvecid, sentvec, metadata={'sentvecid': sentvecid})
        json_cell = {'id': sentvecid, 'sent': sent}
        coll.insert(json_cell)
        #pdb.set_trace()
        return 0


#
import traceback
def sents2vec(gen, coll, bc, library):
    '''
    read data from gen
    fetch vec from sent
    save date into mongo
    '''
    print('sents2vec')
    for sents in gen:
        try:
            arrs = bc.encode(sents)
        except:
            traceback.print_exc()
            print(sents)
            continue
        for sent,sentvec in zip(sents,arrs):
          try:
            sentvecid = genarate_mongo_id(sent)
            weather_sent_exist = search_in_mongo(coll, 'id', sentvecid)
            if not len(weather_sent_exist) == 0:
                logger.info('there is one in db: %s'%sent)
                continue
            library.write(sentvecid, sentvec, metadata={'sentvecid': sentvecid})
            json_cell = {'id': sentvecid, 'sent': sent}
            coll.insert(json_cell)
            logger.info('insert %s'%sent)
          except:
              traceback.print_exc()
              print(sents)
              continue


def clr(instring):
    instring = re.sub('[\r\n]','',instring)
    instring = re.sub(' ','',instring)
    instring.strip()
    return instring


def readSentFromMongo(sent, coll, library):
    try:
        sentvecid = genarate_mongo_id(sent)
        weather_sent_exist = search_in_mongo(coll, 'id', sentvecid)
        response = library.read(sentvecid)
        return (weather_sent_exist, response.data, response.metadata)
    except:
        return (-1, -1, -1)


def trans_guangdian_address_into_vec(coll, library, bc, fn='/home/siy/data/广电全量地址_weak.csv'):
    lines = open(fn,'r').readlines()
    for line in lines:
        line = strQ2B(line)
        line = clr(line)
        for i in range(len(line)):
            for j in range(len(line)-i):
                if i+j < len(line):
                    sent = line[i:i+j]
                    if len(sent)>0 and len(sent)<len(line):
                        append_one(sent, coll, library, bc)


if __name__ == '__main__':
    sent = sys.argv[1]
    lib, c, db, coll = init()
    bc = init_bert()
    gen = read_csv_from_data()
    print('read_csv_from_data gen ready')
    sents2vec(gen, coll, bc, lib)
    #weather_sent_exist, response.data, response.meta_data = readSentFromMongo(sent, coll, lib)
    trans_guangdian_address_into_vec(coll, lib, bc, fn='/home/siy/data/广电全量地址_weak.csv')
    #print(gen.__next__())
    #test_get_one_from_guizhou(coll)
    # test_get_all_arr(coll, lib)
