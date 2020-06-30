#!/bin/bash

if [ $# -lt 1 ]; then
	echo "illegal number of parameters, use e.g."
	echo "./eval.sh REFERENCE_FILE"
	echo "	-o: overall instead of line by line"
	exit 1
fi


REFERENCE="$1"
#HYPOTHESIS="$2"

for HYPOTHESIS in `find "../SpaCy/output_spacy/" "../SEM/output_sem/" "../Perdido/output_perdido/" "../CoreNLP/output_corenlp/" "../CasEN/output_casen/" -name "hypo_*.txt"`

do


# by default grep add line numbers
GREP_ADD_LINE_NUMBER="n"

# if there is a third parameter
if [ "$OVERALL_INSTEAD_OF_LINE_BY_LINE" == "-o" ]; then
    # do not append line numbers to grep matches
	GREP_ADD_LINE_NUMBER=""
fi

function eval_corpus() {
	name="$1"
	regex=$2
	
	# set of reference entities
	set_reference="set_reference_$name.txt"

	# set of hypothesis entities
	set_hypothesis="set_hypothesis_$name.txt"
		
	# correct entities
	intersection="set_intersection_$name.txt"
	
	# reference
	grep -o$GREP_ADD_LINE_NUMBER -P $regex "$REFERENCE"  |\
	      sed 's/.*/\L&/'                                |\
	      iconv -f utf8 -t ascii//TRANSLIT               |\
	      sort > "/tmp/$set_reference"

	# hypothesis
	grep -o$GREP_ADD_LINE_NUMBER -P $regex "$HYPOTHESIS"       |\
	      sed -e 's|\(<[^>]*>\) |\1|g ; s| \(</[^>]*>\)|\1|g ' |\
	      sed 's/.*/\L&/' | iconv -f utf8 -t ascii//TRANSLIT   |\
	      sort > "/tmp/$set_hypothesis"
	
	echo $HYPOTHESIS
	# number of retrived entities
	n_hypothesis=$(wc -l "/tmp/$set_hypothesis" | awk -F" " '{print $1}')
	echo "$name retrived entities (tp+fp): $n_hypothesis"
	
	# to avoid division by zero calculating the precision	
	if [ $n_hypothesis == "0" ]; then
	  n_hypothesis=0.00000001
	fi
	
	# number of relevant entities
	n_reference=$(wc -l "/tmp/$set_reference" | awk -F" " '{print $1}')
	echo "$name relevant entities (tp+fn): $n_reference"
		
	# ref (intersection) hypothesis
	comm -12 "/tmp/$set_reference" "/tmp/$set_hypothesis" | sort -n > "/tmp/$intersection"

	# number of correct entitites
	n_true_positive=$(wc -l "/tmp/$intersection" | awk -F" " '{print $1}')
	echo "$name true positive entities (tp): $n_true_positive"

	precision=$(echo "scale=3 ; $n_true_positive/$n_hypothesis" | bc)
	echo "$name precision tp/(tp+fp): $precision"
	
	# to avoid division by zero calculating the fscore	
	if [ $precision == "0" ]; then
	  precision=0.00000001
	fi

	recall=$(echo "scale=3 ; $n_true_positive/$n_reference" | bc)
	echo "$name recall tp/(tp+fn): $recall"

	fscore=$(echo "scale=3 ; 2*(($precision*$recall)/($precision+$recall))" | bc)
	echo "$name fscore 2*((p*r)/(p+r)): $fscore"
		
	echo "========================================================="
	 >> scores.txt

}
eval_corpus "location" \<placeName\>.*?\<\/placeName\> 
done 