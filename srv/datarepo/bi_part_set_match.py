#!

import json

def set_add(str1,str2):
  ret = set(str1) & set(str2)
  return ret

def mark(str1,str2):
  addset = set_add(str1,str2)
  mark_1 = ""
  mark_2 = ""
  for i in str1:
    if i in addset:
      mark_1+="I"
    else:
      mark_1+="O"
  for j in str2:
    if j in addset:
      mark_2+="I"
    else:
      mark_2+="O"
  return str1,mark_1,str2,mark_2
  

