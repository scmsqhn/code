#!
import re
import mylog
from mylog import logger

def is_max(input_item,max_value):
    return input_item[1] == max_value

def strQ2B(ustring):
    ustring = str(ustring)
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12200:
            inside_code = 32
        elif inside_code >= 65281 and inside_code <= 65374:
            inside_code -= 65248
        rstring+=chr(inside_code)
    #return re.sub("[^\u4e00-\u9fa50-9A-Za-z]","",rstring)
    return rstring

def get_nums(line):
    return "CUT".join(re.findall("([a-zA-Z\d]+|号楼|号院|单元|楼|层|附\d+号|栋)",line))

def get_chars_nums(line):
    return "CUT".join(re.findall("[\da-zA-Z]+",line))

def clr(line):
    line = strQ2B(line)
    #line = re.sub("与.+?交叉.+?米","",line)
    #line = re.sub("[^u4e00-\u9fa5a-z0-9A-Z]","",line)
    return line.strip()

def without_num(line):
    print("过滤前",line)
    line = strQ2B(line)
    line = re.sub("[\da-zA-Z]+号[楼院]?"," ",line)
    line = re.sub("[\d一-十]+单元"," ",line)
    line = re.sub("\d+层"," ",line)
    line = re.sub("[\da-zA-Z]+栋"," ",line)
    line = re.sub("[\da-zA-Z]+栋"," ",line)
    line = re.sub("[^\u4e00-\u9fa5]+"," ",line)
    print("过滤后",line)
    return line

def before_first_num(line):
    return re.split("\d+",line)[0]

def numbers(line):
    return re.findall("\d+",line)

def first_numbers(line):
    nums = re.findall("\d+",line)
    if len(nums)>0:
        return nums[0]
    return ""

def minEditDist(sm, sn):
  m,n = len(sm)+1, len(sn)+1
  matrix = [[0]*n for i in range(m)]
  """长度为字符串长度+1"""
  matrix[0][0] = 0
  for i in range(1,m):
      matrix[i][0] = matrix[i-1][0] + 1
  for j in range(1,n):
      matrix[0][j] = matrix[0][j-1] + 1
  """第一行第一列分别为0开始,1自增序列"""
  const = 0
  for i in range(1,m):
    for j in range(1,n):
      if sm[i-1] == sn[j-1]:
        cost = 0
      else:
        cost = 1 #替换的权重 1
      """这里分别对应与增加,删除,替换"""
      """增加 删除的权重 1 """
      matrix[i][j] = min(matrix[i-1][j]+1,matrix[i][j-1]+1,matrix[i-1][j-1]+cost)
      logger.debug(str(i)+","+str(j)+","+str(matrix[i][j]))
  logger.debug(str(matrix[m-1][n-1]))
  return matrix[m-1][n-1]

if __name__ == "__main__":
  minEditDist("ab","abc")
