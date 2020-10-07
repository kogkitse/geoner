# GeoNER

*GeoNER* was developed within the project *Cité de Dames* at the University of Gustave Eiffel to perform location named entities recognition in French. It calls and uses five tools: Perdido, SEM, SpaCy, CoreNLP and CasEN. GeoNER creates and normalizes the output files of each tool in a specific predefined nomination and repertory.


## User's instructions for first time use.

1. Download geoner-master to your private directory from https://github.com/kogkitse/geoner/archive/master.zip

2. Set a corpus (raw and tagged text) into geoner-master/Corpus/corpus_name/. 
Your tagged corpus should be in TEI format, for example : 
\<placeName\>Paris\<\/placeName\>. If other tags other than placeName are included 
this is not a problem for further processing. 

3. Use Corpus/preprocessing_tagged_ref/preprocessing_corpus_ref.py file in order to preprocess your reference tagged file. A file with a "ref" prefix will be created into your corpus file.  

5. Open <em>GeonNER.py</em> file and replace inside os.system your own python executable.


7. Inside geoner-master/CoreNLP folder you should download and unzip the stanford-ner-4.0.0 directory. Please download and follow instructions for installation from: https://nlp.stanford.edu/software/stanford-ner-4.0.0.zip. You should also need to download a french classifier from : http://nlp.stanford.edu/software/stanford-corenlp-4.1.0-models-french.jar

8. In order to call <em>Perdido's API</em> you should create your own key. Please visit http://erig.univ-pau.fr/PERDIDO/demonstration and register yourself in order to receive your own key. Please set your key into line 14, variable <em>apiKey</em>.

9. For <em>SEM</em> you should install a Firefox geckodriver. https://selenium-python.readthedocs.io/installation.html

10. <em>CasEN</em> is a module of  Unitex, a grammar-based corpus processing suite. Please install Unitex from: https://unitexgramlab.org/
Launch Unitex and set French, then Info => Preferences and check your private directory in dictionnaire tab. Copy link and close Unitex. Open CasEN/casen.py and set line 17 to 22 with your own directories.


## Execution 

Install all requirements with 

    pip install -r requirements.txt

Run GeonNER.py, for example: 
    
    > GeoNER.py raw_corpus.txt tagged_corpus.txt


## Evaluation 

To perform the evaluation you need a reference corpus (manually tagged corpus). In order to obtain the accuracy, recall and f-measure scores run the ./eval.sh script followed by the reference’s filename corpus. Evaluation script run in linux terminal. In case you work in windows you can install a cygwin terminal. You may need to install "bc package". Set master directory inside evaluation/eval.sh at line 21.

For example: 

    $ ./eval.sh REFERENCE_FILE HYPOTHESIS_CORPUS_NAME

The script generates a score file with scores from tool’s files and files containing true positives, false negatives and positives for every hypothesis’s file. It is possible to specify only one input file by changing the hypothesis variable in the script.

---- 
**Important**:

To obtain the results of the evaluation script it is important to ensure a strict alignment at sentence level between the reference and hypothesis corpora.
     
*preprocessing_corpus.py* script allows you to make the necessary substitutions to the corpus to be processed in order to obtain the alignment between the reference and the hypothesis corpora.

Some other scripts are also delivered for corpus processing inside ./Corpus/preprocessing_tagged_ref/.


 
---- 
