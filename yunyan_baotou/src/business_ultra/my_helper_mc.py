import sys
import os
sys.path.append('/data/yunyan_baotou/src')

import myjieba_posseg.posseg as posseg
import function_ultra.utils_bt as utils_bt


def address_formula(line1):
    line = line1
    res_tmp = utils_bt.pre_trans(line)
    line = list(res_tmp.keys())[0]
    res_final = posseg.my_jieba_cut(line)
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

    return  res_final


if __name__ == "__main__":
    address_test = '内蒙古自治区包头昆区钢18街坊佳园小区24号楼1单元9号'
    address_cut = address_formula(address_test)
    print(address_cut)
