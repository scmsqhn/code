#!/usr/bin/env python
# coding: utf8
"""Load vectors for a language trained using fastText
https://github.com/facebookresearch/fastText/blob/master/pretrained-vectors.md
Compatible with: spaCy v2.0.0+
句子输入=>汉字=>768维度的向量=>保存成spacy可以用的向量包
"""
from __future__ import unicode_literals
import numpy as np
import re
from spacy.language import Language
import spacy
import plac
from bert_serving.client import BertClient
from mylogger import logger
import traceback

bc = BertClient(
    ip="192.168.1.64",
    show_server_config=True,
    timeout=100000,
    port=5555,
    port_out=5556)
logger.info('init bert SUCC')

# "/home/siy/Downloads/guizhou/new/csv",


def clr(line):
    line = re.sub('[^\u4e00-\u9fa50-9a-zA-Z]', '', line)
    return line


def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring


@plac.annotations(
    lang=(
        "Optional language ID. If not set, blank Language() will be used.",
        "positional",
        None,
        str))
def main(
        lang=None):
    if lang is None:
        nlp = Language()
    else:
        # create empty language class – this is required if you're planning to
        # save the model to disk and load it back later (models always need a
        # "lang" setting). Use 'xx' for blank multi-language class.
        nlp = spacy.blank(lang)
    file_loc = './广电全量地址.txt'
    #file_loc = '/home/siy/Downloads/guizhou/new/txt/0.txt'
    nr_dim = 768
    nlp.vocab.reset_vectors(width=int(nr_dim))
    cnt=0
    with open(file_loc, 'r') as f:
        # df = pd.read_csv(f)
        lines = f.readlines()
        np.random.shuffle(lines)
        lines = lines[:10000]
        for line in lines:
            # line = line.decode()
            # print(line)
            line = strQ2B(line)
            line.strip()
            line = clr(line)
            line.strip()
            vecs = []
            try:
                print(line)
                vecs = bc.encode(list(line))
            except:
                traceback.print_exc()
                print(list(line))
                continue
            for char, vec in zip(line, vecs):
                try:
                    nlp.vocab.set_vector(ord(char), bc.encode([char]))
                except BaseException:
                    traceback.print_exc()
                    print(char)
                    continue
            cnt += 1
            print('bingo,  i write in %s' % cnt)
    nlp.to_disk('./zh_models')

if __name__ == '__main__':
    plac.call(main)
