#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse


import os, sys, platform
from os import path

file = sys.argv[1]

basename = os.path.basename(file) 
directory = os.path.dirname(sys.argv[0])
corpus_dir = os.path.dirname(file)
dir_corpusname = os.path.basename(corpus_dir)
base_prefix = os.path.splitext(basename)[0]
hypo_create_path = path.join(directory+"/output_corenlp/ouput_"+dir_corpusname)

#check if 'hypo_create_path' exists already
if not os.path.exists(hypo_create_path):
    os.makedirs(hypo_create_path)

base_rename_extention_txt = "{}".format('output_' + base_prefix + '.txt')
base_rename_extention_tsv = "{}".format('output_' + base_prefix + '.tsv')

hypo_output_path_txt = path.join(directory+"/output_corenlp/ouput_"+dir_corpusname, base_rename_extention_txt)
hypo_output_path_tsv = path.join(directory+"/output_corenlp/ouput_"+dir_corpusname, base_rename_extention_tsv)


os.chdir(".\CoreNLP\stanford-ner-4.0.0")
#check if the system is Windows or Linux
if platform.system() == "Windows":
    os.system("java -mx1000m -cp stanford-ner.jar;lib/* edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers\\french-wikiner-4class.crf.ser.gz -textFile " + file +' > '+ hypo_output_path_txt) 
    os.system("java -mx1000m -cp stanford-ner.jar;lib/* edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers\\french-wikiner-4class.crf.ser.gz  -outputFormat tabbedEntities -textFile " + file +' >' + hypo_output_path_tsv)
else: 
    os.system("java -mx600m -cp stanford-ner.jar:lib/* edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers/french-wikiner-4class.crf.ser.gz -textFile " + file +' > '+ hypo_output_path_txt)
    os.system("java -mx600m -cp stanford-ner.jar:lib/* edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers/french-wikiner-4class.crf.ser.gz -outputFormat tabbedEntities -textFile " + file +' >' + hypo_output_path_tsv)

os.chdir("..")

os.system("D:/Apps/Anaconda/envs/myenv/python.exe d:/CiteDames/GeoNER-tools/CoreNLP/output_processing.py " + file)
