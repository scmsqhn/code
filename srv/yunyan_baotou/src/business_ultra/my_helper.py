import sys
import os
sys.path.append(os.environ['WORKBENCH'])
sys.path.append(os.environ['ROOT'])
sys.path.append(os.environ['YUNYAN'])
sys.path.append('../..')
import myconfig
import business_ultra
import myjieba_posseg
import myjieba_posseg.posseg as posseg
import function_ultra.utils_bt as utils_bt
import re
import pdb

def address_formula(line1):
    line = line1.strip()
    res_tmp = utils_bt.pre_trans(line)
    line = list(res_tmp.keys())[0]
    kvs = res_tmp[line]
    print(line)
    res_final = posseg.my_jieba_cut(line)
    print(res_final)
    if line1.find('内蒙古自治区') >= 0:
        if line1.find('包头市') >= 0:
            res_final = '内蒙古自治区/PROV 包头市/CITY '+res_final
        else:
            res_final = '内蒙古自治区/PROV 包头/CITY ' + res_final
    else:
        if line1.find('包头市') >= 0:
            res_final = '内蒙古/PROV 包头市/CITY ' + res_final
        else:
            res_final = '内蒙古/PROV 包头/CITY ' + res_final
    #res_final = re.sub(".\+?街坊/XIAOQU ","",res_final)
    res_final = re.sub("内蒙古/PROV ","内蒙古自治区/PROV ",res_final)
    res_final = re.sub("包头/CITY ","包头市/CITY ",res_final)
    
    return back_trans(kvs,res_final)

def back_trans(kvs,res_final):
    for k in kvs:
        v = kvs[k]
        res_final = re.sub(k,v,res_final)
    return res_final

if __name__ == "__main__":
    address_test = '内蒙古自治区包头市青山区育才小区二段16栋408号'
    address_cut = address_formula(address_test)
    print(address_cut)
