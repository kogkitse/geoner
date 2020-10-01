# -*- coding: utf-8 -*-
# Project Cité des Dames 
# Author : kogkitse
# Attention : before declare your file to process you should apply this file
# the preprocessing script located into Corpus directory, in order to obtain line alignement!

import sys, os, re, shutil 
from os import path


file = sys.argv[1]
basename = os.path.basename(file) 
directory = os.path.dirname(sys.argv[0])
base_origin_prefix = os.path.splitext(basename)[0]


# copy-paste and rename file
new_file = os.path.dirname(sys.argv[1]) + "\\" + base_origin_prefix + "_GeoNER_repair.txt"
shutil.copy(file, new_file)

basename = os.path.basename(new_file) 
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

file = open_doc(new_file)
match_endline = r"$"
sub = " {S}"
file_endline = re.sub(match_endline, sub, file, 0, re.MULTILINE)
file_text_path = path.join(private_dir+'\\Corpus\\'+basename)
with open(file_text_path, "w", encoding="utf-8") as file_text_path: 
    file_text_path.write(file_endline)

# # Analyse CasEN Geo
os.system('mkdir "'+input_corpus+base_prefix+'_snt"')

# normalise input
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Normalize "'+private_dir+'\\corpus\\'+base_prefix+'.txt" "-r'+unitexFrenchFolder+'Norm.txt" "--output_offsets='+private_dir+'\\corpus\\'+base_prefix+'_snt\\normalize.out.offsets" -qutf8-no-bom"')

# tokenise input
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Tokenize "'+unitexFrenchFolder+'corpus\\'+base_prefix+'.snt" "-a'+unitexFrenchFolder+'Alphabet.txt" "--input_offsets='+unitexFrenchFolder+'corpus\\'+base_prefix+'_snt\\normalize.out.offsets" "--output_offsets='+unitexFrenchFolder+'Corpus\\'+base_prefix+'_snt\\tokenize.out.offsets" -qutf8-no-bom"')


# apply lexical resources
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Dico "-t'+unitexFrenchFolder+'Corpus\\'+base_prefix+'.snt" "-a'+unitexFrenchFolder+'Alphabet.txt" "-m'+dela_system+'\\profession.bin"  "'+dela_system+'\\profession.bin" "'+dela_system+'\\Dela_fr.bin" "'+unitexFrenchFolder+'Dela\\CasEN_Ambiguites-.bin"  "'+unitexFrenchFolder+'Dela\\CasEN_Dico.bin" "'+unitexFrenchFolder+'Dela\\ditex-cities-fr.bin" "'+unitexFrenchFolder+'Dela\\Prolex-Unitex-BestOf_2_2_fra.bin" -qutf8-no-bom"')



# run cassys 
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Cassys  "-a'+unitexFrenchFolder+'Alphabet.txt" "-t'+unitexFrenchFolder+'Corpus\\'+base_prefix+'.snt" "-l'+unitexFrenchFolder+'Cassys\\CasEN_analyse_GEO.csc" "-w'+dela_system+'\\Dela_fr.bin" "-w'+dela_system+'\\Prolex-Unitex_1_2.bin" -v -r'+unitexFrenchFolder+'Graphs\\ "--input_offsets='+unitexFrenchFolder+'Corpus\\'+base_prefix+'_snt\\normalize.out.offsets" -qutf8-no-bom"')


# extract output
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Concord "'+unitexFrenchFolder+'Corpus\\'+base_prefix+'_snt\\concord.ind" "-m'+unitexFrenchFolder+'Corpus\\'+base_prefix+'-raw.txt" -qutf8-no-bom"')

# # Synthesize analyse CasEN GEO output

os.system('mkdir "'+input_corpus+base_prefix+'_csc_snt"')
# normalize input
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Normalize "'+unitexFrenchFolder+'corpus\\'+base_prefix+'_csc.txt" "-r'+unitexFrenchFolder+'Norm.txt" "--output_offsets='+private_dir+'\\corpus\\'+base_prefix+'_csc_snt\\normalize.out.offsets" -qutf8-no-bom"')


# tokenize input
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Tokenize "'+unitexFrenchFolder+'corpus\\'+base_prefix+'_csc.snt" "-a'+unitexFrenchFolder+'Alphabet.txt" -qutf8-no-bom"')

# run cassys synthesize
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Cassys  "-a'+unitexFrenchFolder+'Alphabet.txt" "-t'+unitexFrenchFolder+'Corpus\\'+base_prefix+'_csc.snt" "-l'+unitexFrenchFolder+'Cassys\\CasEN_synthese_TEI.csc" "-w'+dela_system+'\\Dela_fr.bin" -v -r'+unitexFrenchFolder+'Graphs\\ "--input_offsets='+unitexFrenchFolder+'Corpus\\'+base_prefix+'_csc_snt\\normalize.out.offsets" -qutf8-no-bom"')

# extract output
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Concord "'+unitexFrenchFolder+'Corpus\\'+base_prefix+'_csc_snt\\concord.ind" "-m'+unitexFrenchFolder+'Corpus\\'+base_prefix+'_TEI.txt" -qutf8-no-bom"')

# # post processing clean output 

output = unitexFrenchFolder+'Corpus\\'+base_prefix+'_TEI.txt'
output_file = open_doc(output)

match_unitex_tags = r"\{S\} | \{S\}|\{S\}"
match_placetag = r"(<|</)(placeName|geogName)>(<|</)(placeName|geogName)>"
match_punct = r"\n|\)|\(|\[|\]|»|«|…"
match_split = r"(\.(?<![A-Z]\.)\s*|\!\s*|\?\s*)(\w|<|«|»)"

# Substitute punctuation in order to split sentences line by line
subst_unitex_tags = ""
subst_placetag = "\\1placeName>"
subst_punct_split = ""
subst_match_split = "\\1\\n\\2"

result_unitex_tags= re.sub(match_unitex_tags, subst_unitex_tags, output_file, 0, re.MULTILINE)
result_placetags = re.sub(match_placetag, subst_placetag, result_unitex_tags, 0, re.MULTILINE)
result_punct = re.sub(match_punct, subst_punct_split, result_placetags, 0, re.MULTILINE)
result_split = re.sub(match_split, subst_match_split, result_punct, 0, re.MULTILINE)



# write output to output_casen directory
corpus_dir = os.path.dirname(sys.argv[1])
dir_corpusname = os.path.basename(corpus_dir)
hypo_create_path = path.join(directory+"/output_GeoNER_repair/ouput_"+dir_corpusname)

# Check if 'hypo_create_path' existe already
if not os.path.exists(hypo_create_path):
    os.makedirs(hypo_create_path)

# base_rename_extention = "{}".format('hypo_GeoNER_repair_' + base_origin_prefix + '.txt')
output_path = (hypo_create_path+'//GeoNER_repair_' + base_origin_prefix + '.txt')
# print(output_path)
with open(output_path, "w", encoding="utf-8") as hypothesis: 
    hypothesis.write(result_split)

# Analyse Geo and create file GeoNER 


file_with_tags = open_doc(output_path)
basename_tag_file = os.path.basename(output_path) 
base_prefix_tag_file = os.path.splitext(basename_tag_file)[0]
match_endline = r"$"
sub = " {S}"
file_endline = re.sub(match_endline, sub, file_with_tags, 0, re.MULTILINE)
file_text_path = path.join(private_dir+'\\Corpus\\'+basename_tag_file)
with open(file_text_path, "w", encoding="utf-8") as file_text_path: 
    file_text_path.write(file_endline)

# # Analyse Geo and create file GeoNER with unitex 
os.system('mkdir "'+input_corpus+base_prefix_tag_file+'_snt"')

# normalise input
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Normalize "'+private_dir+'\\corpus\\'+base_prefix_tag_file+'.txt" "-r'+unitexFrenchFolder+'Norm.txt" "--output_offsets='+private_dir+'\\corpus\\'+base_prefix_tag_file+'_snt\\normalize.out.offsets" -qutf8-no-bom"')

# tokenise input
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Tokenize "'+unitexFrenchFolder+'corpus\\'+base_prefix_tag_file+'.snt" "-a'+unitexFrenchFolder+'Alphabet.txt" "--input_offsets='+unitexFrenchFolder+'corpus\\'+base_prefix_tag_file+'_snt\\normalize.out.offsets" "--output_offsets='+unitexFrenchFolder+'Corpus\\'+base_prefix_tag_file+'_snt\\tokenize.out.offsets" -qutf8-no-bom"')

# apply lexical resources
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Dico "-t'+unitexFrenchFolder+'Corpus\\'+base_prefix_tag_file+'.snt" "-a'+unitexFrenchFolder+'Alphabet.txt" "-m'+dela_system+'\\profession.bin" "-m'+dela_system+'\\Prolex-Unitex_1_2.bin" "-m'+dela_system+'\\Dela_fr.bin" "-m'+unitexFrenchFolder+'Dela\\CasEN_Ambiguites-.bin" "-m'+unitexFrenchFolder+'Dela\\CasEN_Dico.bin" "-m'+unitexFrenchFolder+'Dela\\Prolex-Unitex-BestOf_2_2_fra.bin" "'+dela_system+'\\Dela_fr.bin" "'+dela_system+'\\motsGramf-.bin" "'+dela_system+'\\Prolex-Unitex_1_2.bin" "'+unitexFrenchFolder+'Dela\\CasEN_Ambiguites-.bin" "'+unitexFrenchFolder+'Dela\\CasEN_Dico.bin" "'+unitexFrenchFolder+'Dela\\ditex-cities-fr.bin" "'+unitexFrenchFolder+'Dela\\Prolex-Unitex-BestOf_2_2_fra.bin" -qutf8-no-bom"')

# apply graph of correction
os.system('CMD /c ""'+unitex_directory + 'UnitexToolLogger.exe" Locate "-t' + unitexFrenchFolder + 'Corpus\\'+ base_prefix_tag_file+'.snt" "'+ unitexFrenchFolder + '\Graphs\GeoNER_CasEN\Correction_placeNameTOplaceName.fst2" "-a'+ unitexFrenchFolder + 'Alphabet.txt" -L -R --all "-m'+ dela_system + '\\profession.bin" "-m'+ dela_system + '\\Prolex-Unitex_1_2.bin" "-m'+ dela_system + '\\Dela_fr.bin" "-m'+dela_system+'\\motsGramf-.bin" "-m' + unitexFrenchFolder + 'Dela\\CasEN_Ambiguites-.bin" "-m' + unitexFrenchFolder + 'Dela\\CasEN_Dico.bin" "-m' + unitexFrenchFolder + 'Dela\\ditex-cities-fr.bin" "-m' + unitexFrenchFolder + 'Dela\\Prolex-Unitex-BestOf_2_2_fra.bin" -b -Y --stack_max=1000 --max_matches_per_subgraph=200 --max_matches_at_token_pos=400 --max_errors=50 -qutf8-no-bom"')

# extract output
os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Concord "'+unitexFrenchFolder+'Corpus\\'+base_prefix_tag_file+'_snt\\concord.ind" "-m'+unitexFrenchFolder+'Corpus\\'+base_prefix_tag_file+'-raw.txt" -qutf8-no-bom"')




output_hypo_file = hypo_create_path+'//hypo_GeoNER_' + base_origin_prefix + '.txt'
output_file = unitexFrenchFolder+'Corpus\\'+base_prefix_tag_file+'-raw.txt'
result_unitex_tags = re.sub(match_unitex_tags, subst_unitex_tags, open_doc(output_file), 0, re.MULTILINE)
with open(output_hypo_file, "w", encoding="utf-8") as hypothesis: 
    hypothesis.write(result_unitex_tags)
# shutil.copy(unitexFrenchFolder+'Corpus\\'+base_prefix_tag_file+'-raw.txt' , output_hypo_file)