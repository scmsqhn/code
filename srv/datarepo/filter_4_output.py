import re
import numpy as np

lines = open("./output/output_zz.txt","r").readlines()
g = open("for_check_zz.txt","w+")
for line in lines:
    sample = re.findall("^\D+?(\D\D\d+)\D+?(\d+)",line)
    predict = re.findall("ROOT\D+?(\D\D\d+)\D+?(\d+)",line)
    #_sample = re.findall("^\D+?(\D\D\d+)\D+?",line)
    #_predict = re.findall("ROOT\D+?(\D\D\d+)\D+?",line)
    #_sample_ = re.findall("^.+?(\D\D\d+).+?",line)
    #_predict_ = re.findall("ROOT.+?(\D\D\d+).+?",line)
    if len(sample)>0 and len(predict)>0:
        if predict[0] == sample[0]:
            g.write("%s\n"%line)
            continue
    """
    if len(_sample)>0 and len(_predict)>0:
        if _predict[0] == _sample[0]:
            g.write("%s\n"%line)
            continue
    """
    #elif len(_sample_)>0 and len(_predict_)>0:
    #    if _predict_[0] == _sample_[0]:
    #        g.write("%s\n"%line)
    #        continue
    if len(re.findall("\d+",line)) == 0:
        g.write("%s\n"%line)
        continue
    g.write("%s, ROOTNone\n"%line.split("ROOT")[0])
g.close()
            
