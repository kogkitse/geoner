#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse

# Preprocessing script will create two files:
# ref_filename.txt and raw_filename.txt with splitted punctuation
# line by line 

import re
from pathlib import Path
import os
from os import path
import re
import sys

file = sys.argv[1]


# Read file
def read_doc(filename): 
    with open(filename, 'r', encoding='utf-8') as file:
        read_line = file.read()
        return read_line

def match(read_line):
    match_punct = r"\n|\)|\(|\[|\]|»|«|…"
    match_split = r"(\.\s?|\!\s?|\?\s?)(\w)"
    # Substitute punctuation in order to split sentences line by line
    subst_punct_split = ""
    subst_match_split = "\\1\\n\\2"

    split_corpus = re.sub(match_punct, subst_punct_split, read_line, 0, re.MULTILINE)
    split_lines = re.sub(match_split, subst_match_split, split_corpus, 0, re.MULTILINE)
    return split_lines 

basename = os.path.basename(file) 
directory = os.path.dirname(sys.argv[1])
base_prefix = os.path.splitext(basename)[1]
output_path = path.join(directory, "ref_"+basename)

prepocessing = match(read_doc(file))
print(prepocessing)
with open(output_path, 'w', encoding='utf-8') as output:
    output.write(match(prepocessing))