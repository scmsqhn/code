# ================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: data_helper.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-04-29
#   describe:
# -*- coding:utf-8 –*-
'''
程序用来将excel批量转换为csv文件。指定源路径和目标路径。
在main函数中指定源文件路径source，目标文件路径ob.
这个程序假设Excel文件放在：D:\CDDE
输出csv文件到：D:\cc
'''

# 导入pandas
import pandas as pd
import os
import traceback

# 建立单个文件的excel转换成csv函数,file 是excel文件名，to_file 是csv文件名。
def excel_to_csv(file, to_file):
    try:
        data_xls = pd.read_excel(file, sheet_name=0)
        data_xls.to_csv(to_file, encoding='utf_8_sig')
    except:
        traceback.print_exc()


# 读取一个目录里面的所有文件：
def read_path(path):
    dirs = os.listdir(path)
    return dirs

# 主函数


# 目标文件路径
ob = "/home/siy/Downloads/guizhou/new/csv"

# 源文件路径
source = "/home/siy/Downloads/guizhou/new"


def main(source, ob):
    # 将源文件路径里面的文件转换成列表file_list
    """
    gen = os.walk(source)
    file_list = []
    for dir, _, files in gen:
        for file in files:
            file_list.append(os.path.join(dir, file))
    """
    file_list = [source + '/' + i for i in read_path(source)]
    print(file_list)
    j=1
    # 建立循环对于每个文件调用excel_to_csv()
    for it in file_list:
        # 给目标文件新建一些名字列表
        j_mid=str(j)
        j_csv=ob + '/' + j_mid + ".csv"
        print(it, j_csv)
        excel_to_csv(it, j_csv)
        j=j + 1


if __name__ == '__main__':
    main(source, ob)
