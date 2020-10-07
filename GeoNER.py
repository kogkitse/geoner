#!\usr\bin\env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse

# entry arguments : python GeoNER.py raw_corpus tagged_corpus 


import re, os, sys
from pathlib import Path
from os import path

# Raw corpus
entry_corpus = sys.argv[1]
# Tagged reference corpus
entry_tagged_corpus = sys.argv[2]

is_file = os.path.is_file(entry_corpus)
is_ref_file = os.path.is_ref_file(entry_tagged_corpus)

# If entry is not a file but a folder then first condition will take place

if is_file == False :
    for src_filename in os.listdir(entry_corpus):
        entry = (entry_corpus +'\\'+ src_filename)
        # Run spaCy classification
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\Spacy\Call_spaCy.py " + entry)
        # Run Perdido classification 
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\Perdido\Call_Perdido.py " + entry)
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\Perdido\perdido_hypo_postprocessing.py " + entry)
        # Run CoreNLP
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\CoreNLP\\Call_Corenlp.py " + entry)
        # Run CasEN
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\CasEN\casen.py " + entry)
        # Run GeoNER_repair
        # os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\GeoNER_repair\GeoNER_repair.py " + entry)
        # Run SEM classification 
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\SEM\Call_SEM.py " + entry)
elif is_ref_file == False :
    for src_filename in os.listdir(entry_tagged_corpus):       
        #Run preprocessing_corpus_ref in order to align reference tagged corpus to hypothesis output
        os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\Corpus\preprocessing_tagged_ref\preprocessing_corpus_ref.py " + entry_tagged_corpus)
else :
    # Run spaCy classification
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\Spacy\Call_spaCy.py " + entry_corpus)
    # Run Perdido classification 
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\Perdido\\Call_Perdido.py " + entry_corpus)
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\Perdido\perdido_hypo_postprocessing.py " + entry_corpus)
    # Run CoreNLP
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\CoreNLP\\Call_Corenlp.py " + entry_corpus)
    # Run CasEN
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\CasEN\casen.py " + entry_corpus)
    # Run GeoNER_repair
    # os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\GeoNER_repair\GeoNER_repair.py " + entry_corpus)
    # Run SEM classification 
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\SEM\Call_SEM.py " + entry_corpus)

    # Run preprocessing_corpus_ref.py in order to align reference tagged corpus to hypothesis output
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe .\Corpus\preprocessing_tagged_ref\preprocessing_corpus_ref.py " + entry_tagged_corpus)
