#
import pandas as pd
import jieba

def read_csv(filename,fileout):
  f = open(fileout,"a+")
  lines = pd.read_csv(filename).iloc[5838936:,1]
  for line in lines:
    if not pd.notnull(line):
      continue
    print(line)
    words = jieba.cut(line)
    for word in words:
      f.write("%s "%word)
    f.write("\n")

read_csv("./data/test/eval_zz.csv", "./data/std/eval_zz.txt")
