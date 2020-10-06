#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse


from pathlib import Path
import sys, os, re, shutil
import pandas as pd  
from os import path


# Enter coprus file, for example : 
# ./create_csv_iob.py ../Margot_wikisource_20200825\MargueriteDeValois-original.txt 
corpus_dir = os.path.dirname(sys.argv[1])
dir_corpusname = os.path.basename(corpus_dir)
basename = os.path.basename(sys.argv[1]) 
basename_prefix = os.path.splitext(basename)[0]

casen_file = './CasEN/output_casen/ouput_' + dir_corpusname +'\hypo_casEN_' + basename_prefix +'_IOB.csv'
spacy_file = './Spacy/output_spacy/ouput_' + dir_corpusname +'\\hypo_spaCy_' + basename_prefix + '_IOB.csv'
corenlp_file = './CoreNLP/output_corenlp/ouput_' + dir_corpusname +'\\hypo_CoreNLP_' + basename_prefix + '_IOB.csv'
sem_file = './SEM/output_sem/ouput_' + dir_corpusname +'\\hypo_SEM_' + basename_prefix + '_IOB.csv'
perdido_file = './Perdido/output_perdido/ouput_' + dir_corpusname +'\hypo_Perdido_' + basename_prefix + '_IOB.csv'
geoner_file = './GeoNER_repair/output_GeoNER_repair/ouput_' + dir_corpusname +'\hypo_GeoNER_' + basename_prefix + '_IOB.csv'
ref_file = input("Set reference tagged corpus : ")


words = [] 
tags_spacy = []   
tags_sem = []   
tags_casen = []   
tags_perdido = []   
tags_corenlp = []   
tags_geoner = []
tags_ref = []

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
matches_words = re.finditer(regex_words, open_doc(casen_file), re.MULTILINE)
# add words in a list
for match_word in matches_words:
    words.append(match_word.group())

output_path = path.join("./evaluation/files/"+ basename_prefix +'/'+ basename_prefix + "_words.csv")
df = pd.DataFrame(list(zip(words)))
df.to_csv(output_path, encoding='utf-8', index=False)

#  match tags of csv file
regex_tags = r"O$|B-LOC|I-LOC"
matches_tags_spacy = re.finditer(regex_tags, open_doc(spacy_file), re.MULTILINE)
matches_tags_sem = re.finditer(regex_tags, open_doc(sem_file), re.MULTILINE)
matches_tags_casen = re.finditer(regex_tags, open_doc(casen_file), re.MULTILINE)
matches_tags_corenlp = re.finditer(regex_tags, open_doc(corenlp_file), re.MULTILINE)
matches_tags_perdido = re.finditer(regex_tags, open_doc(perdido_file), re.MULTILINE)
matches_tags_geoner = re.finditer(regex_tags, open_doc(geoner_file), re.MULTILINE)
matches_tags_ref = re.finditer(regex_tags, open_doc(ref_file), re.MULTILINE)

casen_tag = tags_in_list(tags_casen, matches_tags_casen)
sem_tag = tags_in_list(tags_sem, matches_tags_sem)
spacy_tag = tags_in_list(tags_spacy, matches_tags_spacy)
perdido_tag = tags_in_list(tags_perdido, matches_tags_perdido)
corenlp_tag = tags_in_list(tags_corenlp, matches_tags_corenlp)
geoner_tag = tags_in_list(tags_geoner, matches_tags_geoner)
ref_tag = tags_in_list(tags_ref, matches_tags_ref)
print(geoner_tag)

output_path = path.join("./evaluation/files/"+ basename_prefix +'/'+ basename_prefix + "_tags.csv")
df = pd.DataFrame(list(zip(spacy_tag)))
df.to_csv(output_path, encoding='utf-8', index=False)

# create a dataframe with words and tags from each tool's output
df = pd.DataFrame(list(zip(words, spacy_tag, casen_tag, sem_tag, perdido_tag, corenlp_tag, geoner_tag, ref_tag)), 
columns =['Word', 'Spacy_tag', 'CasEN_tag', 'SEM_tag', 'Perdido_tag', 'CoreNLP_tag', 'Geoner_tag', 'Reference_tag'])

# save output in IOB format from dataframe to csv
output_path = path.join("./evaluation/files/"+ basename_prefix +'/'+ basename_prefix + "_IOB.csv")
df.to_csv(output_path, encoding='utf-8', index=False)
print("Output created at : " + "./evaluation/files/"+ basename_prefix )