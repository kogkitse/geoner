#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse

# Script splitting text up to 3000 sentences in seperate files
# Script source : https://stackoverflow.com/a/17749339



import glob, sys, os
from os import path


folder = sys.argv[1]

read_files = glob.glob(folder + '*plain_Part_*.txt')
print(read_files)
corpus_dir = os.path.dirname(folder)
dir_corpusname = os.path.basename(corpus_dir)

hypo_create_path = path.join(corpus_dir + "\output_perdido\\" + dir_corpusname)

with open('hypo_perdido_MDV-Tome1_plain.txt' , "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())