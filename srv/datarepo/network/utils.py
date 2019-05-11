import re


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

def clr(line):
    line = strQ2B(line)
    line = re.sub("与.+?交叉.+?米","",line)
    line = re.sub("[^u4e00-\u9fa5a-z0-9A-Z]","",line)
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
