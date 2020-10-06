#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse 
# 

import re
from pathlib import Path
import os
from os import path
import sys
import json

entry_arg = sys.argv[1]



def read_doc(filename): 
    with open(filename, 'r', encoding='utf-8') as file:
        read_line = file.read()
        return read_line

   
dic = []
first_words = []
i = 0
file_content = read_doc(entry_arg)
dico_content = read_doc('D:\\CiteDames\GeoNER-tools\\Corpus\preprocessing_tagged_ref\plain_dico.txt')
dic.append(dico_content)

file_content = file_content.replace(',\n', ',\n@@@')
line_list =  re.split(r',?\s*\n+', file_content)
line_list = [line.replace('@@@', ', ') for line in line_list]


#print(line_list)

# dico entries
dico_content = dico_content.strip().split('\n')  
dico_item = [d.split()[0] for d in dico_content]

# Verify manually in or not dico words
# first_word = [i.split()[0] for i in line_list]
# not_dico = [string for string in first_word if string not in dico_item]
# in_dico = [string for string in first_word if string in dico_item]
# print(in_dico)

# loop over each line
line_previous_last_word_is_punctuation = False
for index, line in enumerate(line_list):
    first_word_index = 0 
    # test if the line begins with a colon
    if line.startswith(','):
        first_word_index = 1

    # get the first word
    first_word = line.split(' ')[first_word_index]

    # test wheanever the first word exist or not in dico
    if first_word not in dico_item:
        # build a new line by lowercasing the first (common) word
        # 1) line begins with a colon
        if first_word_index != 0:
            line_new = ", " + first_word.lower() + " " + ' '.join(line.split(' ')[first_word_index+1:])
            # replace the old line with the new one
            line_list[index] = line_new
        # 2) the last line does not finish with a punctuation character    
        elif line_previous_last_word_is_punctuation == False:
            # sentence without colon
            line_new = first_word.lower() + " " + ' '.join(line.split(' ')[first_word_index+1:])
            # replace the old line with the new one
            line_list[index] = line_new
  
    # keep trace of the last word character
    if len(line) > 0:
        line_previous_last_word_char = line.split(' ')[-1][-1]
        line_previous_last_word_is_punctuation = bool(not re.match('^[a-zA-Z0-9]*$',line_previous_last_word_char))
    else:
        line_previous_last_word_is_punctuation = False


with open ("output_filename.txt", "w", encoding='utf-8') as file_out :
    for index, line in enumerate(line_list):
        line_next_first_word_is_punctuation = True
        # test if there is a next line
        if index+1 < len(line_list):
            # if there is a next line, test when the first word is a puncuation character
            line_next = line_list[index+1].strip()
            if len(line_next) > 0:
                line_next_first_word_char = line_next.split(' ')[0][0]
                line_next_first_word_is_punctuation =  bool(not re.match('^[a-zA-Z0-9]*$',line_next_first_word_char))

        # rstrip : remove any white spaces at the end of the string
        line = line.strip()

        # if the next line word begins with a space, do not append a trailing space
        if line_next_first_word_is_punctuation == True:
            file_out.write("%s" % line)
        else:
            file_out.write("%s " % line)
exit(0)
