#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse

import pandas as pd
from pathlib import Path
import os
from os import path
import re
import sys

file_corpus = sys.argv[1] 

file_tsv = r'D:\\CiteDames\\GeoNER-tools\\CoreNLP\\output_corenlp\\output.tsv'
data_tsv = file_tsv.encode("ansi").decode("utf-8")
file_txt = r'D:\\CiteDames\\GeoNER-tools\\CoreNLP\\output_corenlp\\output.txt'
data_txt = file_txt.encode("ansi").decode("utf-8")

#  Read file line by line
def open_doc(filename): 
    with open(filename) as file:
        read_line = file.read()
        return read_line

def tsv_LOC_tags(data_tsv) :
    # # Match LOC tags 
    match_LOC = r"^([^\t]*)\tI-LOC"
    # Match any other tag
    match_other_tag = r"\t|\n\n"
    # Match '?,.,!'
    match_punct = r"(\.\s?|\!\s?|\?\s?)(\w|«|»)"

    # Substitute LOC tags with <placeName>
    subst_LOC = "<placeName>\\1</placeName> "
    # Substitute LOC tags with nothing
    subst_other_tag = ""
    # Substitute punctuation in order to split sentences line by line
    subst_punct_split = "\\1\\n\\2"

    result_LOC = re.sub(match_LOC, subst_LOC, data_tsv, 0, re.MULTILINE)
    result_hypo = re.sub(match_other_tag, subst_other_tag, result_LOC, 0, re.MULTILINE)
    result_hypo_split = re.sub(match_punct, subst_punct_split, result_hypo, 0, re.MULTILINE)
    return result_hypo_split

def txt_LOC_tags(data_txt) :
    # # Match LOC tags 
    match_LOC = r"\s([^/]*)/I-LOC"
    # Match any other tag
    match_other_tag = r"/(?!placeName)[^\s+]*|\n|\)|\(|\[|\]|»|«|…"
    # Match '?,.,!'
    match_punct = r"(\.\s*|\!\s*|\?\s*)(\w|<)"

    # Substitute LOC tags with <placeName>
    subst_LOC = " <placeName>\\1</placeName>"
    # Substitute LOC tags with nothing
    subst_other_tag = ""
    # Substitute punctuation in order to split sentences line by line
    subst_punct_split = "\\1\\n\\2" 

    result_LOC = re.sub(match_LOC, subst_LOC, data_txt, 0, re.MULTILINE)
    result_hypo = re.sub(match_other_tag, subst_other_tag, result_LOC, 0, re.MULTILINE)
    result_hypo_split = re.sub(match_punct, subst_punct_split, result_hypo, 0, re.MULTILINE)
    return result_hypo_split


def save_output_files(data):
    # # Save hypothesis' txt output into \output_spacy\file
    basename = os.path.basename(file_corpus) 
    base_prefix = os.path.splitext(basename)[0]
    directory = os.path.dirname(sys.argv[0])
    base_rename_extention_tsv = "{}".format('hypo_CoreNLP_' + base_prefix + '.tsv')
    base_rename_extention_txt = "{}".format('hypo_CoreNLP_' + base_prefix + '.txt')
    hypo_output_path_tsv = path.join(directory+"\output_corenlp", base_rename_extention_tsv)
    hypo_output_path_txt = path.join(directory+"\output_corenlp", base_rename_extention_txt)

    # hypo_output_path.open("w", encoding="utf-8").write(result_hypo_split)
    with open(hypo_output_path_tsv, 'w', encoding='utf-8') as hypo_tsv, open (hypo_output_path_txt, 
    "w", encoding='utf-8') as hypo_txt:
        hypo_tsv.write(tsv_LOC_tags(data_tsv))
        hypo_txt.write(txt_LOC_tags(data_txt))


data_tsv = open_doc(file_tsv)
match_tsv_tags = tsv_LOC_tags(data_tsv)
save_tsv = save_output_files(match_tsv_tags)
data_txt = open_doc(file_txt)
match_txt_tags = txt_LOC_tags(data_txt)
save_txt = save_output_files(match_txt_tags)

# print(match_txt_tags)