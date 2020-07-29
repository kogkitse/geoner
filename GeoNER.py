#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse


import re, os, sys
from pathlib import Path
from os import path

entry_arg = sys.argv[1]

isfile = os.path.isfile(entry_arg)
if isfile == False :
    for src_filename in os.listdir(entry_arg):
        entry = (entry_arg +'\\'+ src_filename)
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
else :
    # Run spaCy classification
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe d:/CiteDames/GeoNER-tools/Spacy/Call_spaCy.py " + entry_arg)
    # Run Perdido classification 
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\Perdido\\Call_Perdido.py " + entry_arg)
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\Perdido\perdido_hypo_postprocessing.py " + entry_arg)
    # Run CoreNLP
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\CoreNLP\\Call_Corenlp.py " + entry_arg)
    # Run CasEN
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\CasEN\casen.py " + entry_arg)
    # Run SEM classification 
    os.system("D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\SEM\Call_SEM.py " + entry_arg)