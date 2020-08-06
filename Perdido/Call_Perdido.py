# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"

import glob, os, re, sys, json, requests, time
import requests_cache
from nltk.tokenize import sent_tokenize
from os import path

requests_cache.install_cache('perdido_cache')

# Please replace the API key below by your own (get it from the dashboard of Dandelion)
apiKey = "faHfUX2B4L"

# urlBegin_1 ="http://erig.univ-pau.fr/PERDIDO/api/nerc/txt_xml/?lang=French&api_key="+apiKey+"&content="
# urlBegin_2 ="http://erig.univ-pau.fr/PERDIDO/api/toponyms/txt_json/?lang=French&api_key="+apiKey+"&content="
urlBegin_3 = "http://erig.univ-pau.fr/PERDIDO/api/geoparsing/?lang=French&api_key="+apiKey+"&content="

#text = ["Je sortis par la porte qui ouvre sur la Seine, et ne repris haleine que dans la rue, par laquelle on va du Petit Pont à la place Saint-Michel, et qu’on appelle, je crois, la rue de la Calandre.","De là je gagnai la place Saint-Germain, et j’arrivai au puits encore toute émue.","Quelle belle cérémonie ! Elle eut lieu le 25 décembre 496, dans l’église de Reims.","Mais une fois, dans un combat qu’il livrait aux Allemands, à Tolbiac, se voyant près de succomber, il invoqua hautement le Dieu de madame Clotilde","Mais en arrivant près de Châlons, on apprit que la Saône avait débordé à plusieurs endroits, et que la navigation était difficile, surtout en revenant de Lyon."]
file = sys.argv[1]


# Create the result file to write inside
# outputXML = open("D:\CiteDames\Perdido/results_url_XML.txt", "w", encoding="utf-8")
# outputJSON = open("D:\CiteDames\Perdido/results_url_JSON.txt", "w", encoding="utf-8")

# Save xml output to file
basename = os.path.basename(file) 
directory = os.path.dirname(sys.argv[0])
base_prefix = os.path.splitext(basename)[0]
corpus_dir = os.path.dirname(file)
dir_corpusname = os.path.basename(corpus_dir)
hypo_create_path = path.join(directory+"/output_perdido/ouput_"+dir_corpusname)

# Check if 'hypo_create_path' existe already
if not os.path.exists(hypo_create_path):
    os.makedirs(hypo_create_path)

base_rename_extention = "{}".format(base_prefix + '.xml')
output_path = path.join(hypo_create_path, "Perdido_" + base_rename_extention)
output = open(output_path, "w", encoding="utf-8")

#i = 0

# Treat the first sentence of the text and calls itself on the remaining sentences after waiting 2 seconds
def analyseRemainingSentences(text):
   # loop over senteces
   for i, sentence in enumerate(text):
      # check if sentence isn't empty
      if len(text) > 0:
         # analyze the sentence using the Perdido API
         # try to call the API every 2 seconds until get a 200 response
         while True:
            print("\n\nAnalyzing « " + sentence + " »"+" No: " + str(i+1))
            # Analyze it with the Perdido API
            # response_1 = requests.get(urlBegin_1 + sentence)
            # response_2 = requests.get(urlBegin_2 + sentence)
            response_3 = requests.get(urlBegin_3 + sentence)
            if response_3.status_code == 200:
               break
            # wait for 2 seconds before analyzing the next sentence
            time.sleep(2)

         # save the full result
         if response_3.text:
            # outputXML.writelines(response_1.text)
            # outputJSON.writelines(response_2.text)
            output.writelines(response_3.text)
        
def open_doc(file): 
    with open(file, encoding='utf-8') as file:
        read_line = file.read()
        return read_line

# Open and read a file line by line
with open(file, 'r', encoding="utf8") as file:
   text = file.read()
   match_punct =r"…"
   subst_punct = ""
   text = re.sub(match_punct, subst_punct, text, 0, re.MULTILINE)

#  Nltk tokenizer split text into sentences
   text = (sent_tokenize(text))
   
# Start analyzing the text
analyseRemainingSentences(text)
# outputXML.close
# outputJSON.close
output.close

# Clean xml to get txt with placeName tags



