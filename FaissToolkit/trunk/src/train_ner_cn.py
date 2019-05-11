# -*-coding:utf-8-*-
# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Example of training spaCy's named entity recognizer, starting off with an
existing model or a blank model.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function
import os
os.system('pip install plac')
import plac
import random
from pathlib import Path
import spacy
import numpy as np
# import pdb
# training data
import train_data_gen
TRAIN_DATA = [
    ('大家好,我叫鲁智深', {
        'entities': [(4, 6, 'PERSON')]
    }),
    ('我非常喜欢北京和上海.', {
        'entities': [(5, 7, 'LOC'), (8, 10, 'LOC')]
    })
]
#TRAIN_DATA = list(train_data_gen.read_ner_train_data().items())[:-20]
#EVAL_DATA = list(train_data_gen.read_ner_train_data().items())[-20:]


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))

def main(model=os.path.join(os.environ['ROOT'], 'models/ner'), \
    output_dir=os.path.join(os.environ['ROOT'], 'models/ner'), \
    n_iter=10):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('ner')  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe('ner')

    # add labels
    TRAIN_DATA = list(train_data_gen.read_ner_train_data().items())[:-20]
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)

    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
        print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])
        break
    del TRAIN_DATA

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)
        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        EVAL_DATA = list(train_data_gen.read_ner_train_data().items())[-20:]
        for text, _ in EVAL_DATA:
            doc = nlp2(text)
            print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
            print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

def init_model_4_pred(output_dir):
    nlp2 = spacy.load(output_dir)
    return nlp2

def test(texts, nlp2):
    results = []
    for text in texts:
        doc = nlp2(text)
        # pdb.set_trace()
        results.append([(ent.text, ent.label_) for ent in doc.ents])
        #print('Entities', [(print(ent.text), print(ent.label_)) for ent in doc.ents])
        #[(print(ent.text), print(ent.label_)) for ent in doc.ents]
        #print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])
    return results

def predict():
    nlp = init_model_4_pred('/tmp/neraddr/ner')
    #text = '北京西路12号'
    #EVAL_DATA = list(train_data_gen.read_ner_train_data().items())[-20:]
    #texts = [text for text,_ in EVAL_DATA]
    with open('output.txt', 'w+') as g:
        with open('train_source_address.txt', 'r') as f:
            lines = f.readlines()
            np.random.shuffle(lines)
            for line in lines[:1000]:
                print(line)
                results = test([line], nlp)
                for result in results:
                    g.write(line)
                    for items in test([line], nlp):
                        for item in items:
                            g.write(item[0] + ":" + item[1] + "\n")
                g.write("==============")
                # pdb.set_trace()
                # pdb.set_trace()
                # g.write(test([line],nlp2))
                # g.write("\n"+"==================")

    #doc = test(text, nlp2)
    #print('Entities', [(ent.text, ent.label_) for ent in doc.ents])

    # Expected output:
    # Entities [('Shaka Khan', 'PERSON')]
    # Tokens [('Who', '', 2), ('is', '', 2), ('Shaka', 'PERSON', 3),
    # ('Khan', 'PERSON', 1), ('?', '', 2)]
    # Entities [('London', 'LOC'), ('Berlin', 'LOC')]
    # Tokens [('I', '', 2), ('like', '', 2), ('London', 'LOC', 3),
    # ('and', '', 2), ('Berlin', 'LOC', 3), ('.', '', 2)]

if __name__ == '__main__':
    plac.call(main)
    predict()
