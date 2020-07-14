:: In order to run the bat echo "run_corenlp corpus_file"
:: Enter into corenlp file and run java commande, 
cd .\stanford-ner-4.0.0 
set filename=%1
:: Set basename of input filename in order to create outputpath
for /F %%i in ("%filename%") do set basename=%%~ni
mkdir ..\output_corenlp\output_%basename%
set output_dir=..\output_corenlp\output_%basename%
java -mx1000m -cp stanford-ner.jar;lib/* edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers\french-wikiner-4class.crf.ser.gz -textFile %filename% > %output_dir%\output_%basename%.txt
java -mx1000m -cp stanford-ner.jar;lib/* edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers\french-wikiner-4class.crf.ser.gz  -outputFormat tabbedEntities -textFile %filename% > %output_dir%\output_%basename%.tsv
cd ..
D:/Apps/Anaconda/envs/myenv/python.exe d:/CiteDames/GeoNER-tools/CoreNLP/output_processing.py %filename%