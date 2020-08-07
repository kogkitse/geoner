#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse

# Script splitting text up to 3000 sentences in seperate files
# Script source : https://stackoverflow.com/a/16290652

import re, os, sys
from pathlib import Path
from os import path
from nltk.tokenize import sent_tokenize
from itertools import islice


# Read file
def read_doc(filename): 
    with open(filename, 'r', encoding='utf-8') as file:
        read_line = file.read()
        return read_line

entry_corpus = sys.argv[1]

basename = os.path.basename(entry_corpus) 
base_prefix = os.path.splitext(basename)[0]
corpus_dir = os.path.dirname(entry_corpus)
dir_corpusname = os.path.basename(corpus_dir)

corpus_read = read_doc(entry_corpus)
text = (sent_tokenize(corpus_read))

sorting = True
hold_lines = []
for row in text:
    hold_lines.append(row + ' ')
outer_count = 1
line_count = 0
while sorting:
    count = 0
    increment = (outer_count-1) * 3000
    left = len(hold_lines) - increment
    file_name = base_prefix + "_Part_" + str(outer_count * 1) + ".txt"
    hold_new_lines = []
    if left < 3000:
        while count < left:
            hold_new_lines.append(hold_lines[line_count])
            count += 1
            line_count += 1
        sorting = False
    else:
        while count < 3000:
            hold_new_lines.append(hold_lines[line_count])
            count += 1
            line_count += 1
    outer_count += 1
    output_path = path.join(corpus_dir + '\\' + file_name)
    with open(output_path, 'w', encoding='utf-8') as next_file:
        for row in hold_new_lines:
            next_file.write(row)