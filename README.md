# GeoNER

*GeoNER* was developed within the project *Cité de Dames* at the University of Gustave Eiffel to perform location named entities recognition in French. It calls and uses five tools: Perdido, SEM, SpaCy, CoreNLP and CasEN. GeoNER creates and normalizes the output files of each tool in a specific predefined nomination and repertory.


## Preliminaries

**CasEN**: Please install Unitex and place into your Unitex’s private directory Casen_GEO files and set files into ./CasEN/casen.py.

**Perdido**:  Please fill with your own key the “apiKey” line 14.

**SEM**: Instructions for installations are at the beginning of Call_SEM.py file. 


## Execution 

On Windows or Linux, *GeoNER.py* file will execute these tools followed by the filename to be processed.  For example: 
    
    > GeoNER.py raw_corpus.txt tagged_corpus.txt


## Evaluation 

To perform the evaluation you need a reference corpus (manually tagged corpus). In order to obtain the accuracy, recall and f-measure scores run the eval.sh script followed by the reference’s filename corpus.
For example: 

    > ./eval.sh REFERENCE_FILE HYPOTHESIS_CORPUS_NAME

The script generates a score file with scores from tool’s files and files containing true positives, false negatives and positives for every hypothesis’s file. It is possible to specify only one input file by changing the hypothesis variable in the script.

---- 
**Important**:

To obtain the results of the evaluation script it is important to ensure a strict alignment at sentence level between the reference and hypothesis corpora.
     
*preprocessing_corpus.py* script allows you to make the necessary substitutions to the corpus to be processed in order to obtain the alignment between the reference and the hypothesis corpora.

---- 
