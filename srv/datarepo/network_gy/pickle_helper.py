#
import pickle

def demo():
    """ first in first out """
    f =open("pickle.txt","wb+")
    lists = [123,'zhongwen',[456]]
    strs = 'zifuchuan'
    num = 123
 
    pickle.dump(lists,f)
    pickle.dump(strs,f)
    pickle.dump(num,f)
    f.close()
    f =open("pickle.txt","rb+")
    
    lists2= pickle.load(f)
    strs2= pickle.load(f)
    num2 = pickle.load(f)
    f.close()

    print(num2, strs2,lists2) 

def save(filename,vs):
    """ save in the list """
    f =open(filename,"wb+")
    for v in vs:
        pickle.dump(v,f)
    f.close()

def load(filename,ks):
    """ load into the list """
    res = []
    f =open(filename,"rb+")
    for k in ks:
        res.append(pickle.load(f))
    f.close()
    return res
