import os
from bert_serving.client import BertClient
import traceback
import time
import arctic
from arctic import Arctic
import quandl
# Connect to Local MONGODB
store = Arctic('localhost')
# Create the library - defaults to VersionStore
store.initialize_library('bert2vec')
# Access the library
library = store['bert2vec']
## Load some data - maybe from Quandl
#aapl = quandl.get("WIKI/AAPL", authtoken="your token here")
# Store the data in the library
# Reading the data
PATH = '.'
bc = BertClient(ip='58.17.133.80', show_server_config=True, timeout=10000, port=18087, port_out=15005)
import pymongo
c = pymongo.MongoClient(host='localhost', port=27017)
db = c.bert2vec
coll = db.guizhou
ks,vs = [],[]
for _,_,filenames in os.walk(PATH):
  for filename in filenames:
    if not filename in ['train.tsv','test.csv','eval.tsv']:
        continue
    for line in open(os.path.join(PATH,filename),'r').readlines():
        try:
            print("RIGHT "+line)
            kv = line.split('\t')
            assert(len(kv)==2)
            k,v = kv[1],kv[0]
        except:
            traceback.print_exc()
            print("WRONG "+line)
            continue
        ks.append(k.strip())
        vs.append(v.strip())
        #if len(ks)==1:
        if True:
            if ks=='':
                ks=' '
            if vs=='':
                vs=' '
            sentsvec = []
            try:
                sentsvec = bc.encode(ks)
            except:
                print(ks)
                continue
            lbsvec = bc.encode(vs)
            for sentvec,lbvec,k,v in zip(sentsvec,lbsvec,ks,vs):
                time_ = str(int(time.time())) + str(hash(k))
                sentvecid = time_ + '_0',
                lbvecid = time_ + '_1',
                library.write(sentvecid[0], sentvec, metadata={'sentvecid':sentvecid })
                library.write(lbvecid[0], lbvec, metadata={'lbvecid': lbvecid})
                json_cell = {
                              'id'      :str(int(time.time())) + str(hash(k)),
                              'sent'    :k,
                              'lb'      :v,
                              'sentvec' :sentvecid,
                              'lbvec'   :lbvecid
                            }
                print(coll.insert(json_cell))
            ks,vs = [],[]
#item = library.read('AAPL')
#aapl = item.data
#metadata = item.metadata
