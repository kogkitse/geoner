:: In order to run the bat echo "run_ner corpus_file"
:: Enter into corenlp file and run java commande, 
cd .\stanford-ner-4.0.0 
set filename=%1
java -mx1000m -cp stanford-ner.jar;lib/* edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers\french-wikiner-4class.crf.ser.gz -textFile %filename% > ..\output_corenlp\output.txt
java -mx1000m -cp stanford-ner.jar;lib/* edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers\french-wikiner-4class.crf.ser.gz  -outputFormat tabbedEntities -textFile %filename% > ..\output_corenlp\output.tsv
cd ..
D:/Apps/Anaconda/envs/myenv/python.exe d:/CiteDames/GeoNER-tools/CoreNLP/output_processing.py %filename%