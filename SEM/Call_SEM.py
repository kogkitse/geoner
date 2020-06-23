#!/usr/bin/env python
# coding: utf8
# Project : "Cité des dames : créatrices dans la cité"

import glob, time
# from nltk.tokenize import sent_tokenize
from io import open
import io

# Install selenium and the Firefox webdriver:
# https://selenium-python.readthedocs.io/installation.html
# Also install the « Firefox » driver 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import re
import os
from os import path
import sys


# The text is provided as a list of sentences
#text = ["Je sortis par la porte qui ouvre sur la Seine, et ne repris haleine que dans la rue, par laquelle on va du Petit Pont à la place Saint-Michel, et qu’on appelle, je crois, la rue de la Calandre.","De là je gagnai la place Saint-Germain, et j’arrivai au puits encore toute émue.","Quelle belle cérémonie ! Elle eut lieu le 25 décembre 496, dans l’église de Reims.","Mais une fois, dans un combat qu’il livrait aux Allemands, à Tolbiac, se voyant près de succomber, il invoqua hautement le Dieu de madame Clotilde","Mais en arrivant près de Châlons, on apprit que la Saône avait débordé à plusieurs endroits, et que la navigation était difficile, surtout en revenant de Lyon."]

# Maximum number of characters used in the webpage
limit = 500000
i = 0
delay = 5
# Treat the first set of sentences which is not larger as the limit
def analyseRemainingSentences(text):
   global i, limit
   selectedText = ""
   
   while len(text)>0 and len(selectedText)+len(text[0]) < limit:
      i += 1
      selectedText += text.pop()+" "
   
   return [selectedText,text]

def readFileIntoString(filename):
   with io.open(filename, mode="r", encoding="utf-8") as file:
      data = file.read()
      return data

   return ""

def savePage(browser,file):
   file = open(file,"w",encoding='utf-8')
   file.write(browser.page_source)
   file.close()


def tag_LOC(output_hypo):
    # Match locations tags
    match_LOC = r"<span id=\"Location\" title=\"Location\">([^<]*)<\/span>"
    # Match every tag except <placeName>
    match_other_tag = r"<(?!placeName|\/placeName)[^>]*>|\n|\)|\(|\[|\]|»|«|…"
    # Match '?,.,!'
    match_punct = r"(\.\s?|\!\s?|\?\s?)(\w|<|«|»)"

    # Substitute Location tags with <placeName>
    subst_LOC = "<placeName>\\1</placeName>"
    # Substitute LOC tags with nothing
    subst_other_tag = ""
    # Substitute punctuation in order to split sentences line by line
    subst_punct_split = "\\1\\n\\2"

    
    result_LOC = re.sub(match_LOC, subst_LOC, output_hypo, 0, re.MULTILINE)
    result_hypo = re.sub(match_other_tag, subst_other_tag, result_LOC, 0, re.MULTILINE)
    result_hypo_split = re.sub(match_punct, subst_punct_split, result_hypo, 0, re.MULTILINE)
    return(result_hypo_split)



#assert "Python" in driver.title

def toto(file_name, file_content, output_dir, geckoWebDriver):
   if len(file_content) == 0 :
      return

   # Load the SEM page
   geckoWebDriver.get("http://apps.lattice.cnrs.fr/sem/")
   elem1 = geckoWebDriver.find_element_by_id("textToTag")
   time.sleep(2)
   elem1.clear()
   #print(selectedText)
   geckoWebDriver.execute_script('document.getElementById("textToTag").value="'+file_content.replace('\n',"\\n").replace('"',"''")+'";')

   # Start MEDITE by clicking the submit button
   
   submitButton = geckoWebDriver.find_element_by_css_selector("button[type=submit]")
   submitButton.click()
   time.sleep(120)
   
   otherTab = geckoWebDriver.find_element_by_css_selector("label[for=tab2]")
   otherTab.click()
   time.sleep(delay)

   elem1 = geckoWebDriver.find_element_by_id("content2")
   output_hypo = (elem1.get_attribute('innerHTML'))
   
   # Write output
   basename = os.path.basename(file_name) 
   base_prefix = os.path.splitext(basename)[0]
   base_rename_extention = "{}".format(base_prefix + '.txt')
   output_path = path.join(output_dir, "output_sem", "hypo_SEM_" + base_rename_extention)
   with open(output_path, 'w', encoding='utf-8') as output:
      output.write(tag_LOC(output_hypo))
   
   # hypo_output_path = Path("D:\CiteDames\GeoNER-tools\SEM\output_sem\hypo_SEM_MargueriteDeValois.txt")
   # hypo_output_path.open("w", encoding="utf-8").write(tag_LOC(output_hypo))
   
   folder = os.path.abspath(os.path.dirname(sys.argv[0]))
   savePage(geckoWebDriver,os.path.join(folder,"SEM.html"))

def main():
   output_dir = os.path.dirname(sys.argv[0])
   file_name  = sys.argv[1]

   file_content = readFileIntoString(file_name)
   # print(file_content)

   geckoWebDriver = webdriver.Firefox(executable_path=r'D:\\CiteDames\SEM\\geckodriver.exe')

   toto(file_name, file_content, output_dir, geckoWebDriver)
   
   # geckoWebDriver.close()

if __name__ == "__main__":
   # execute only if run as a script
   main()