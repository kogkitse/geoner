#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse

# entry arguments : pyhton GeoNER.py raw_corpus tagged_corpus 
# for example :  

import re, os, sys
from pathlib import Path
from os import path

entry_corpus = sys.argv[1]
# entry_tagged_corpus = sys.argv[2]

isfile = os.path.isfile(entry_corpus)
if isfile == False :
    for src_filename in os.listdir(entry_corpus):
        entry = (entry_corpus +'\\'+ src_filename)
        # Run spaCy classification
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe d:/CiteDames/GeoNER-tools/Spacy/Call_spaCy.py " + entry)
        # Run Perdido classification 
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\Perdido\\Call_Perdido.py " + entry)
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\Perdido\perdido_hypo_postprocessing.py " + entry)
        # Run CoreNLP
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\CoreNLP\\Call_Corenlp.py " + entry)
        # Run CasEN
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\CasEN\casen.py " + entry)
        # Run SEM classification 
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\SEM\Call_SEM.py " + entry)

        #Run preprocessing_corpus_ref in order to align reference tagged corpus to hypothesis output
        # os.system("D:/Apps/Anaconda/envs/myenv/python.exe d:/CiteDames/GeoNER-tools/Corpus/preprocessing_tagged_ref/preprocessing_corpus_ref.py " + entry_tagged_corpus)
else :
    # Run spaCy classification
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe d:/CiteDames/GeoNER-tools/Spacy/Call_spaCy.py " + entry_corpus)
    # Run Perdido classification 
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\Perdido\\Call_Perdido.py " + entry_corpus)
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\Perdido\perdido_hypo_postprocessing.py " + entry_corpus)
    # Run CoreNLP
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\CoreNLP\\Call_Corenlp.py " + entry_corpus)
    # Run CasEN
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\CasEN\casen.py " + entry_corpus)
    # Run SEM classification 
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\SEM\Call_SEM.py " + entry_corpus)

    # Run preprocessing_corpus_ref.py in order to align reference tagged corpus to hypothesis output
    # os.system("D:/Apps/Anaconda/envs/myenv/python.exe d:/CiteDames/GeoNER-tools/Corpus/preprocessing_tagged_ref/preprocessing_corpus_ref.py " + entry_tagged_corpus)
