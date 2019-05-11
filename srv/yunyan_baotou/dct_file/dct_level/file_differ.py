# coding: utf-8

import codecs
import sys
from pprint import pprint

filepathA = sys.argv[1]
filepathB = sys.argv[2]
a_list = codecs.open(filepathA, "r", "utf-8").read().splitlines()
b_list = codecs.open(filepathB, "r", "utf-8").read().splitlines()
pprint(set(a_list).difference(set(b_list)))
