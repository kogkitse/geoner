#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"

from pathlib import Path
import re
from scrapy import Selector
from os import path
import os
import sys

file = sys.argv[1]



# Read file
def open_doc(filename): 
    with open(filename, 'r', encoding='utf-8') as file:
        read_line = file.read()
        return read_line

def write_doc(filename, text_write):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text_write)

def tag_LOC(output_hypo):
    # Match locations tags
    match_LOC = r"<[^>]*>([^>]*)</w>"
    # Match punct 
    match_punct = r"\n|\)|\(|\[|\]|»|«|…"
    # Match '?,.,!'
    match_split = r"(\.(?<!M\.)\s*|\!\s*|\?\s*)(\w|<)"

    # Substitute Location tags with <placeName>
    subst_LOC = "<placeName>\\1</placeName>"
    # Substitute punct
    subst_punct = ""
    # Substitute punctuation in order to split sentences line by line
    subst_punct_split = "\\1\\n\\2"
    
    result_LOC = re.sub(match_LOC, subst_LOC, output_hypo, 0, re.MULTILINE)
    result_punct = re.sub(match_punct, subst_punct, result_LOC, 0, re.MULTILINE)
    result_hypo_split = re.sub(match_split, subst_punct_split, result_punct, 0, re.MULTILINE)
    return(result_hypo_split)



basename = os.path.basename(file) 
directory = os.path.dirname(sys.argv[0])
base_prefix = os.path.splitext(basename)[0]

base_rename_extention = "{}".format(base_prefix + '.xml')
output_path = path.join(directory+"/output_perdido/ouput_"+base_prefix+"/Perdido_" + base_rename_extention)

# Scrapy lib will call xpath which match every text balise exept //w with @type="NPr"
output = Selector(text = open_doc(output_path))
requete= output.xpath('//w[not(@type="NPr")]/text() | //name[@type="place"]/w | //name[@type="unknown"]/w/text()| //name[@type="person"]/w/text()| //p').extract()
separator = ' '
clean_output = separator.join(requete)
clean_path = path.join(directory+"/output_perdido/ouput_"+base_prefix+"/Perdido_clean_"+ base_rename_extention)
write_doc(clean_path, clean_output)

base_rename_extention = "{}".format(base_prefix + '.txt')
hypo_output_path = path.join(directory+"/output_perdido/ouput_"+base_prefix+"/hypo_perdido_" + base_rename_extention)

write_doc(hypo_output_path, tag_LOC(clean_output))
# with open(hypo_output_path, 'w', encoding='utf-8') as hypo_output:
#     hypo_output.write(tag_LOC(clean_output))
