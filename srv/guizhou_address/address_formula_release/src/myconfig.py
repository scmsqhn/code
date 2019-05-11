#!

import os
import re

CHAR_HASH_DIVIDE = 3000
LENTH_PADDING = 15
TRAIN_DATA = 200000
EVAL_DATA = 300
HASH_MAX = 77777777
CHECK_RULE_JIEDAO = re.compile("\D\D\D[街道路巷村镇坡屯]")
CHECK_RULE_LOUHAO = re.compile("([一二三四五六七八九零]+?[号杠])(?:.*?)?([一二三四五六七八九零]+?[号杠$])")
