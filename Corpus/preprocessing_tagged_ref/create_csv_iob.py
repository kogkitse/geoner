#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse


from pathlib import Path
import sys, os, re, shutil
import pandas as pd  
from os import path

# Enter coprus file
corpus_dir = os.path.dirname(sys.argv[1])
dir_corpusname = os.path.basename(corpus_dir)
basename = os.path.basename(sys.argv[1]) 
basename_prefix = os.path.splitext(basename)[0]

casen_file = './CasEN/output_casen/ouput_' + dir_corpusname +'\hypo_casEN_' + basename_prefix +'_IOB.txt'
print(casen_file)
spacy_file = './Spacy/output_spacy/ouput_' + dir_corpusname +'\\hypo_spaCy_' + basename_prefix + '_IOB.txt'
corenlp_file = './CoreNLP/output_corenlp/ouput_' + dir_corpusname +'\\hypo_CoreNLP_' + basename_prefix + '_IOB.txt'
sem_file = './SEM/output_sem/ouput_' + dir_corpusname +'\\hypo_SEM_' + basename_prefix + '_IOB.txt'
perdido_file = './Perdido/output_perdido/ouput_' + dir_corpusname +'\hypo_Perdido_' + basename_prefix + '_IOB.txt'


words = [] 
tags_spacy = []   
tags_sem = []   
tags_casen = []   
tags_perdido = []   
tags_corenlp = []   

def open_doc(filename): 
    with open(filename, 'r', encoding='utf-8') as file:
        read_line = file.read()
        return read_line

# add tags in a list
def tags_in_list(tags, matches_tags):
    for match_tag in matches_tags:
        tags.append(match_tag.group())
    return tags

#  match words of csv file
regex_words = r"^\w+|^\W"
matches_words = re.finditer(regex_words, open_doc(spacy_file), re.MULTILINE)

# add words in a list
for match_word in matches_words:
    words.append(match_word.group())

#  match tags of csv file
regex_tags = r"O|B-LOC|I-LOC"
matches_tags_spacy = re.finditer(regex_tags, open_doc(spacy_file), re.MULTILINE)
matches_tags_sem = re.finditer(regex_tags, open_doc(sem_file), re.MULTILINE)
matches_tags_casen = re.finditer(regex_tags, open_doc(casen_file), re.MULTILINE)
matches_tags_corenlp = re.finditer(regex_tags, open_doc(corenlp_file), re.MULTILINE)
matches_tags_perdido = re.finditer(regex_tags, open_doc(perdido_file), re.MULTILINE)

casen_tag = tags_in_list(tags_casen, matches_tags_casen)
sem_tag = tags_in_list(tags_sem, matches_tags_sem)
spacy_tag = tags_in_list(tags_spacy, matches_tags_spacy)
perdido_tag = tags_in_list(tags_perdido, matches_tags_perdido)
corenlp_tag = tags_in_list(tags_corenlp, matches_tags_corenlp)


# create a dataframe with words and tags
df = pd.DataFrame(list(zip(words, spacy_tag, casen_tag, sem_tag, perdido_tag, corenlp_tag)), 
columns =['Word', 'Spacy_tag', 'CasEN_tag', 'SEM_tag', 'Perdido_tag', 'CoreNLP_tag'])


