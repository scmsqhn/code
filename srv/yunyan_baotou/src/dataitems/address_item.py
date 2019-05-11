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

class StreetItem(object):
    def __init__(self):
        self.Street_Name_Pre_Modifier = -1
        self.Street_Name = -1
        self.Street_Name_Post_Modifier = -1
        self.Street_Type = -1
        self.Street_Direction = -1
        self.Complete_Street_Name = -1

class ReisidentialItem(object):
    def __init__(self):
        self.Reisidential_Area_Name_Pre_Modifier = -1
        self.Reisidential_Area_Name = -1
        self.Reisidential_Area_Direction = -1
        self.Reisidential_Area_Name_Post_Modifier = -1
        self.Reisidential_Area_Type = -1
        self.Complete_Reisidential_Area_Name = -1

class StreetAddressNumberItem(object):
    def __init__(self):
        self.Street_Address_Number_Prefix = -1
        self.Street_Address_Number = -1
        self.Street_Address_Number_Suffix = -1
        self.Street_Address_Number_Type = -1
        self.Street_Address_Separator_element = -1#分割符
        self.Complete_Street_Address_Number = -1#完整地址
        self.Street_Address_Number_Range = -1#范围

class AddrItem(object):
    def __init__(self):
        self.First_Administrative_Divisions_Name = -1 #国
        self.Second_Administrative_Divisions_Name = -1 #省
        self.Third_Administrative_Divisions_Name = -1 #区
        self.Forth_Administrative_Divisions_Name = -1 #乡
        #---
        self.Multistage_Complete_Street_Name = -1 #[StreetItem()]# 复合街道名 StreetItem complex
        #---小区
        self.MultiComplete_Reisidential_Area_Name = -1 # [ReisidentialItem()]# 复合小区名ReisidentialItem complex
        #---自然村
        self.Natural_Village_Name = -1 # 自然村
        self.Natural_Village_Type = -1 # 自然村类型
        self.Complete_Natural_Village_Name = -1 # 完整自然村名称
        #---地标
        self.Landmark_Name = -1 # 地标性代称
        #---街路巷
        self.Multi_Component_Street_Address_Number = -1 #[StreetAddressNumberItem()]# 复合门牌号
        #---建筑物
        self.Building_Type = -1 # 建筑物完整房屋
        self.Building_Identifier_Number = -1 # 建筑物名称
        self.Building_Element = -1 # 建筑物
        #---
        self.Cell_Type = -1 # 单元类型
        self.Cell_Identifier_Number = -1 # 单元号
        self.Cell_Element = -1 # 单元
        #---
        self.House_Unit_Type = -1 # 房屋类型
        self.House_Unit_Identifier_Number = -1 # 房屋id
        self.House_Unit_Element = -1 # 房租名称
        #---
        self.Complete_Occupancy_Identifier = -1 # 完整使用标识符
        #---
        self.Address_Code = -1
        self.Ultra= -1
        self.Address_X_Coordinate = -1
        self.Address_Y_Coordinate = -1
        self.Address_Longitude = -1
        self.Address_Latitude = -1
        #---
        self.National_Grid_Coordinate = -1
        #---
        self.Address_Z_Value = -1
        self.Address_Classification = -1
        self.Feature_Type = -1
        self.Address_Lifecycle_Status = -1 #['预留','暂定','使用','退休']
        self.Address_Official_Status = -1
        self.Location_Description = -1
        #---
        self.Address_Start_Date = -1
        self.Address_End_Date = -1
        #---
        self.Address_Direct_Source = -1#source
        #---
        self.Address_Authority = -1
        #---
        self.Address_Authority_Code = -1
        self.status = -1
        #---
        self.others = -1

    def state_machine(self):
        '''
        主要的地址要素I包括：行政区划（ADN）、街道名称（SN）、住宅区名称（RAN）、自
然村名称（NVN）、地标名称（LN）、门牌号码（SAN）、建筑物单元房间（BCHU）等七种。
        门牌地址分类提供每类地址的名称、语法、实例、备注说明信息。门牌地址分为四大类：
        —— 街道门牌地址类：按街、路、巷、条、胡同等名称编排门楼牌号。
        —— 住宅区门牌地址类：按住宅小区名称编门楼牌号。
        —— 自然村门牌地址类：以村名称编门楼牌号。
        —— 地标门牌地址类：以地标名称编门楼牌号。
        '''
        self._jiedao_ = []
        self._zhuzhai_ = []
        self._zirancun_ = []
        self._dibiao_ = []

    def sort(type='viterbi'):
        if type=='viterbi':
            #viterbi.viterbi()
            pass

def test():
    ai = AddrItem()
    print(ai,'check ok')

if __name__ == '__main__':
    test()
