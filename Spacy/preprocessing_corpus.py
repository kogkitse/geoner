#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse

# Preprocessing script will create two files:
# ref_filename.txt and raw_filename.txt with splitted punctuation
# line by line 
# echo "preprocessing_corpus.py REFERENCE"

import sys
import re
from pathlib import Path

# Read file
def read_doc(filename): 
    with open(filename, 'r', encoding='utf-8') as file:
        read_line = file.read()
        return read_line

def match(read_line):
    #join into one line
    match_newline = r"\n"
    match_punct = r"(\.\s?|\!\s?|\?\s?)(\w)"
    # Substitute punctuation in order to split sentences line by line
    subst_newline=""
    subst_punct_split = "\\1\\n\\2"
    join = re.sub(match_newline, subst_newline, read_line, 0, re.MULTILINE)
    split = re.sub(match_punct, subst_punct_split, join, 0, re.MULTILINE)
    return split 

def write_doc(filenamepath, split):
    write_path = Path(filenamepath)
    return write_path.open("w", encoding="utf-8").write(split)

file = "/media/sf_CiteDames/GeoNER-tools/Corpus/MémoiresMargueriteDeValois.txt"
filename = read_doc(file)
match = match(filename)
directory = "/media/sf_CiteDames/GeoNER-tools/Corpus/corpus_split.txt"
write = write_doc(directory, match)
