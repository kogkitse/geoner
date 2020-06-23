:: Project Cité des Dames 
:: Script 'run.bat' will execute Spacy, SEM, Perdido and CoreNLP text classification
:: Please type "run corpus_filename" 
:: files with the name 'hypo' contain outputs of execution
:: Author : kogkitse


set INPUT=%1


:: 
:: Run spaCy classification 

D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\Spacy\Call_spaCy.py  %INPUT%

:: Run SEM classification 
D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\Spacy\Call_SEM.py  %INPUT%

:: Run Perdido classification 
D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\Perdido\Call_Perdido.py  %INPUT%

D:\Apps\Anaconda\envs\myenv\python.exe D:\CiteDames\GeoNER-tools\Perdido\perdido_hypo_postprocessing.py

:: Run CoreNLP

D:\CiteDames\GeoNER-tools\CoreNLP\run_corenlp %INPUT%


:: Preprocessing corpus ref

:: D:\Apps\Anaconda\envs\myenv\python.exe D:/CiteDames/GeoNER-tools/preprocessing_corpus.py %INPUT%
