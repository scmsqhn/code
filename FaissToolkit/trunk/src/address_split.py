#================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: address_split.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-05-01
#   describe:

import spacy

def load_ultra_model(model_name='./zh_models'):
    nlp = spacy.load(model_name)
    return nlp

def load_document(nlp, doc_name):
    cont = open(doc_name).read()
    cont = nlp.document(cont)
    print(dir(cont))
    return cont

def test_load_document():
    nlp = load_ultra_model('./zh_models')
    cont = load_document(nlp, '广电全量地址.txt')
    return cont

if __name__=="__main__":
    cont = test_load_document()


