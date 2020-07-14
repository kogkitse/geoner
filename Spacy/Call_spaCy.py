#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"
# author: kogkitse

from __future__ import unicode_literals, print_function
import pickle
import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
from nltk.chunk import conlltags2tree
from spacy import displacy
import os
from os import path
import re
import sys



### Call_spaCy.py corpusfile
# load language model
nlp = spacy.load('fr_core_news_md') 



file = sys.argv[1]

# Read file
def open_doc(filename): 
    with open(filename, 'r', encoding='utf-8') as file:
        read_line = file.read()
        return read_line

doc = nlp(open_doc(file))
# Split text to sentences 
for sent in doc.sents:
    # Tag entities in sentence with labels
    for ent in sent.ents:    
        # HTML visualization with displacy render    
        html_viz = displacy.render([doc], style="ent", page=True)


# Save html output to file
basename = os.path.basename(file) 
directory = os.path.dirname(sys.argv[0])
base_prefix = os.path.splitext(basename)[0]
hypo_create_path = path.join(directory+"/output_spacy/ouput_"+base_prefix)

# Check if 'hypo_create_path' existe already
if not os.path.exists(hypo_create_path):
    os.makedirs(hypo_create_path)

base_rename_extention = "{}".format(base_prefix + '.html')
output_path = path.join(hypo_create_path, "Spacy_" + base_rename_extention)

with open(output_path, 'w', encoding='utf-8') as output:
    output.write(html_viz)

# Remove html balises from output to keep txt with <placeName> tags
#Read html file line by line
html_text = open_doc(output_path)
# Match LOC tags 
match_LOC = r"<mark class=\"entity\" [^>]+\">\s+([^<]*)\n\s+<span [^>]+\">LOC</span>\n</mark>"
# Match any other tag
match_other_tag = r"<mark class=\"entity\" [^>]+\">\s+([^<]*)\n\s+(<span [^>]+\">(PER|ORG|MISC)</span>\n</mark>)|<(?!placeName|\/placeName)[^>]*>|\n|\)|\(|\[|\]|»|«|…|displaCy|^\s+"
# Match '?,.,!'
match_punct = r"(\.(?<!M\.)\s*|\!\s*|\?\s*)(\w|<|«|»)"

# Substitute LOC tags with <placeName>
subst_LOC = "<placeName>\\1</placeName> "
# Substitute LOC tags with nothing
subst_other_tag = "\\1"
# Substitute punctuation in order to split sentences line by line
subst_punct_split = "\\1\\n\\2"

result_LOC = re.sub(match_LOC, subst_LOC, html_text, 0, re.MULTILINE)
result_hypo = re.sub(match_other_tag, subst_other_tag, result_LOC, 0, re.MULTILINE)
result_hypo_split = re.sub(match_punct, subst_punct_split, result_hypo, 0, re.MULTILINE)


# Save hypothesis' txt output into \output_spacy\file
base_prefix = os.path.splitext(basename)[0]
base_rename_extention = "{}".format('hypo_spaCy_' + base_prefix + '.txt')
hypo_output_path = path.join(directory+"/output_spacy/ouput_"+base_prefix, base_rename_extention)

# hypo_output_path.open("w", encoding="utf-8").write(result_hypo_split)
with open(hypo_output_path, 'w', encoding='utf-8') as hypo_output:
    hypo_output.write(result_hypo_split)
