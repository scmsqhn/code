#!
import os
import sys
sys.path.append(os.environ['YUNYAN'])
sys.path.append(os.environ['WORKBENCH'])
import src.function_ultra
from src.function_ultra import viterbi
import pandas as pd

'''
describe finacial
'''
class AddrItem(object):
    def __init__(self):
        self.Sheng= -1 #国
        self.Shi= -1 #省
        self.Qu= -1 #市
        self.SheQu= -1 #社区
        self.CunJuWeiHui = -1 #
        self.ZiRanCunZu = -1 #
        self.JianZhuWuMingCheng = -1 #
        self.MenPaiHao = -1 #
        self.XiaoQuMing = -1 #
        self.ZuTuanMingCheng = -1 #
        self.DongHao = -1 #
        self.LouDongMingCheng = -1 #楼栋名称
        self.DanYuanHao = -1 #
        self.LouCeng = -1 #
        self.HuShiHao = -1 #

def test():
    ai = AddrItem()
    print(ai,'check ok')

if __name__ == '__main__':
    test()
