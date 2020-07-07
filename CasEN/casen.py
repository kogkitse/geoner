# -*- coding: utf-8 -*-
# Project Cité des Dames 
#  Author : kogkitse

import sys, os, re, shutil 
from os import path

file = sys.argv[1]
basename = os.path.basename(file) 
directory = os.path.dirname(sys.argv[0])
base_prefix = os.path.splitext(basename)[0]

# Set directories; In order to find Private dictory's position (Info => Preferencies => Directories) 

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
match_endline = r"$"
sub = " {S}"
file_endline = re.sub(match_endline, sub, file, 0, re.MULTILINE)
file_text_path = path.join(private_dir+'\\Corpus\\'+basename)
with open(file_text_path, "w", encoding="utf-8") as file_text_path: 
    file_text_path.write(file_endline)

# os.system('mkdir "'+input_corpus+base_prefix+'_snt"')

# Normalise input

# os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Normalize "'+private_dir+'\\corpus\\'+base_prefix+'.txt" "-r'+unitexFrenchFolder+'Norm.txt" "--output_offsets='+private_dir+'\\corpus\\'+base_prefix+'_snt\\normalize.out.offsets" -qutf8-no-bom"')

# Tokenise input

# os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Tokenize "'+unitexFrenchFolder+'corpus\\'+base_prefix+'.snt" "-a'+unitexFrenchFolder+'Alphabet.txt" "--input_offsets='+unitexFrenchFolder+'corpus\\'+base_prefix+'_snt\\normalize.out.offsets" "--output_offsets='+unitexFrenchFolder+'Corpus\\'+base_prefix+'_snt\\tokenize.out.offsets" -qutf8-no-bom"')


# Apply lexical resources 

# os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Dico "-t'+unitexFrenchFolder+'Corpus\\'+base_prefix+'.snt" "-a'+unitexFrenchFolder+'Alphabet.txt" "-m'+dela_system+'\\profession.bin" "'+dela_system+'\\profession.bin" "'+dela_system+'\\Dela_fr.bin" "'+unitexFrenchFolder+'Dela\\CasEN_Ambiguites-.bin" "'+unitexFrenchFolder+'Dela\\CasEN_Dico.bin" "'+unitexFrenchFolder+'Dela\\Prolex-Unitex-BestOf_2_2_fra.bin" -qutf8-no-bom"')


# Run cassys 

# os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Cassys  "-a'+unitexFrenchFolder+'Alphabet.txt" "-t'+unitexFrenchFolder+'Corpus\\'+base_prefix+'.snt" "-l'+unitexFrenchFolder+'Cassys\\CasEN_analyse_GEO.csc" "-w'+dela_system+'\\Dela_fr.bin" -v -r'+unitexFrenchFolder+'Graphs\\ "--input_offsets='+unitexFrenchFolder+'Corpus\\'+base_prefix+'_snt\\normalize.out.offsets" -qutf8-no-bom"')


# Extract output

# os.system('CMD /c ""'+unitex_directory+'UnitexToolLogger.exe" Concord "'+unitexFrenchFolder+'Corpus\\'+base_prefix+'_snt\\concord.ind" "-m'+unitexFrenchFolder+'Corpus\\'+base_prefix+'-raw.txt" -qutf8-no-bom"')


# Post processing clean output 

output = unitexFrenchFolder+'Corpus\\'+base_prefix+'-raw.txt'
output_file = open_doc(output)

regex_unitex_tags = r"{S} | {S}|{S}"

regex_tags = r"(\{|(\\\{))+([^,\\]*)(\\,\\.|,.)([^+|\\]*)[^\s]*"
regex_geogName = r"(<|</)geogName>"

subst_unitex_tags = ""
subst_tags = "<\\5>\\3</\\5>"
subst_geogName = "\\1placeName>"

result_unitex_tags= re.sub(regex_unitex_tags, subst_unitex_tags, output_file, 0, re.MULTILINE)
result_tags = re.sub(regex_tags, subst_tags, result_unitex_tags, 0, re.MULTILINE)
result_geogName = re.sub(regex_geogName, subst_geogName, result_tags, 0, re.MULTILINE)


# write output to output_casen directory
base_rename_extention = "{}".format('hypo_casEN_' + base_prefix + '.txt')
outuput_path = (os.path.dirname(sys.argv[0])+"\output_casen\\"+ base_rename_extention)
with open(outuput_path, "w", encoding="utf-8") as hypothesis: 
    hypothesis.write(result_geogName)