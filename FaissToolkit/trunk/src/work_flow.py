# ================================================================
#   Copyright (C) 2019 UltraPower Ltd. All rights reserved.
#   file: work_flow.py
#   mail: qinhaining@ultrapower.com.cn
#   date: 2019-04-26
#   describe:


import spacy

nlp = spacy.load("en")

docs = [
    "Our dream was to bring to Shanghai a tribute event dedicated to China which tells our history and visio.",
    "It was not simply a fashion show, but something that we created especially with love and passion for China and all the people around the world who loves Dolce & Gabbana"
]

for doc in nlp.pipe(docs, batch_size=100, n_threads=3):
    print(list(doc))
    print("*" * 50)
