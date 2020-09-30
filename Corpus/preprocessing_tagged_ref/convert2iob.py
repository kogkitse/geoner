#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse


from pathlib import Path
from os import path
import sys, os, re, shutil 


file = sys.argv[1]
basename = os.path.basename(file) 
directory = os.path.dirname(sys.argv[0])
base_prefix = os.path.splitext(basename)[0]

# set directories; In order to find Private dictory's position (Info => Preferencies => Directories) 

unitex_directory ="C:\\Program Files (x86)\\Unitex-GramLab\\App\\"
private_dir = "C:\\Users\\Public\\Documents\\Unitex-GramLab\\Unitex\\French"
unitex_bin = "C:\\Program Files (x86)\\Unitex-GramLab\\App\\UnitexToolLogger.exe"
dela_private_dir= "C:\\Users\\Public\\Documents\\Unitex-GramLab\\Unitex\\French\\Dela"  
dela_system = "C:\\Program Files (x86)\\Unitex-GramLab\\French\\Dela"
input_corpus = private_dir+'\\Corpus\\'

unitexFrenchFolder="C:\\Users\\Public\\Documents\\Unitex-GramLab\\Unitex\\French\\"


def open_doc(filename): 
    with open(filename, 'r', encoding='utf-8') as file:
        read_line = file.read()
        return read_line

file = open_doc(file)
match_apostr = r"(\w+\’|\w+\')"
match_tiret = r"\s*(-)\s*"
match_split = r"(\w+|[^\w\s])\s"
match_punct = r"(\w+)(,|\.|\?|!|;)\tO|(,|\.|!|\?|;|\"|) (\w+)\tO"
match_punct_2 = r"(,|\.|!|\?|;|:|\")(\w+’?)\t"
match_place = r"<placeName>([^\t]*)\tO\n(^[^<]*)</placeName>(,|.|\!|\?|)\tO"
match_placeN = r"<placeName>([^\t]*)</placeName>(,|;|.|\!|\?|)\tO"
match_empty_O = r"^\s+O|^\s+"
match_empty_line = r"^(?:[\t ]*(?:\r?\n|\r))+"
match_other_tags = r"<[^>]*>"

# Substitute punctuation in order to split words line by line
subst_tiret = "-"
subst_apostr = "\\1 "
subst_punct_split = "\\1\\tO\\n"
subst_punct = "\\1\\3\tO\\n\\2\\4\tO"
subst_punct_tags = "\\1\tO\n\\2\tO"
subst_place = "\\1\tB-LOC\n\\2\tI-LOC\n\\3\tO"
subst_placeN = "\\1 B-LOC\n\\2\tO"
subst_non = ""


result_apostr = re.sub(match_apostr, subst_apostr, file, 0, re.MULTILINE)
result_tiret = re.sub(match_tiret, subst_tiret, result_apostr, 0, re.MULTILINE)
result_split = re.sub(match_split, subst_punct_split, result_tiret, 0, re.MULTILINE)
result_punct = re.sub(match_punct, subst_punct, result_split, 0, re.MULTILINE)
result_place = re.sub(match_place, subst_place, result_punct, 0, re.MULTILINE)
result_placeN = re.sub(match_placeN, subst_placeN, result_place, 0, re.MULTILINE)
result_empty_O = re.sub(match_empty_O, subst_non, result_placeN, 0, re.MULTILINE)
result_empty = re.sub(match_empty_line, subst_non, result_empty_O, 0, re.MULTILINE)
result_other_tags = re.sub(match_other_tags, subst_non, result_empty, 0, re.MULTILINE)
result = re.sub(match_punct, subst_punct_tags, result_other_tags, 0, re.MULTILINE)
result = re.sub(match_punct_2, subst_punct_tags, result, 0, re.MULTILINE)


# write output to output directory
corpus_dir = os.path.dirname(sys.argv[1])
dir_corpusname =  os.path.dirname(sys.argv[1])
hypo_path = path.join(dir_corpusname)


output_path = (hypo_path +'\\'+ base_prefix + '_IOB.csv')

with open(output_path, "w", encoding="utf-8") as hypothesis: 
    hypothesis.write(result)