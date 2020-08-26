#!/bin/bash
# ----------------------------------------------------------------------------
# Project Cité des Dames 
# files with the name 'hypo' contain outputs of execution
# Author : kogkitse
# ----------------------------------------------------------------------------
if [ $# -lt 1 ]; then
	echo "illegal number of parameters, use e.g."
	echo "./eval.sh REFERENCE_FILE HYPOTHESIS_CORPUS_NAME [OPTIONS]"
    echo "Options:"
	echo "	-o: overall instead of line by line"
	exit 1
fi
# ----------------------------------------------------------------------------
# Command line arguments
REFERENCE="$1"
HYPOTHESIS_CORPUS_NAME="${2:-MargueriteDeValois}"
OVERALL_INSTEAD_OF_LINE_BY_LINE="$4"
# ----------------------------------------------------------------------------
# Internal constants
BASE_DIR="/media/sf_CiteDames/GeoNER-tools"
HYPOTHESIS_FILE_DIR="/output_"
HYPOTHESIS_FILE_REGEX="hypo_*.txt"
# ----------------------------------------------------------------------------
WORK_DIR="${BASE_DIR}/evaluation/files/${HYPOTHESIS_CORPUS_NAME?You need an HYPOTHESIS_CORPUS_NAME}"
# if working dir already exists, remove it
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"
# ----------------------------------------------------------------------------
HYPOTHESIS_FILES="${WORK_DIR}/${HYPOTHESIS_CORPUS_NAME}-files.txt"
EVALUATION_RESULT="${WORK_DIR}/${HYPOTHESIS_CORPUS_NAME}-evaluation.csv"
# ----------------------------------------------------------------------------
# clear or create file
echo -n '' > "$EVALUATION_RESULT"
# ----------------------------------------------------------------------------
# Start selecting the set of hypothesis to eval
find "${BASE_DIR}" -name "${HYPOTHESIS_FILE_REGEX}" | grep "${HYPOTHESIS_FILE_DIR}" | grep "_${HYPOTHESIS_CORPUS_NAME}" > "$HYPOTHESIS_FILES"
# ----------------------------------------------------------------------------
# loop over each hypothesis file
while read HYPOTHESIS; do
  HYPOTHESIS_FILENAME=$(basename "$HYPOTHESIS")
  HYPOTHESIS_EXTENSION="${HYPOTHESIS_FILENAME##*.}"
  HYPOTHESIS_FILENAME="${HYPOTHESIS_FILENAME%.*}"
  
  echo "Using hypotesis: $HYPOTHESIS_FILENAME"
  
  # by default grep add line numbers
  GREP_ADD_LINE_NUMBER="n"

  # if there is a third parameter
  if [ "$OVERALL_INSTEAD_OF_LINE_BY_LINE" == "-o" ]; then
      # do not append line numbers to grep matches
      GREP_ADD_LINE_NUMBER=""
  fi
  
  # --------------------------------------------------------------------------
  # Evaluate a single reference-hypothesis
  function eval_corpus() {
      name="$1"
      regex="$2"
      
      # get tool name using hypothesis filename
      tool=$(echo "$HYPOTHESIS_FILENAME" | sed 's/^hypo_\([^_]*\).*$/\1/g')

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

      #false negatives	
      comm -13 /tmp/set_hypothesis_location.txt /tmp/set_reference_location.txt > "${WORK_DIR}/$HYPOTHESIS_FILENAME-fn.txt"


      # ref (intersection) hypothesis
      comm -12 "/tmp/$set_reference" "/tmp/$set_hypothesis" | sort -n > "/tmp/$intersection"

      # number of correct entitites
      n_true_positive=$(wc -l "/tmp/$intersection" | awk -F" " '{print $1}')
      echo "$name true positive entities (tp): $n_true_positive"


      # false positives
      comm -23 /tmp/set_hypothesis_location.txt /tmp/set_reference_location.txt > "${WORK_DIR}/$HYPOTHESIS_FILENAME-fp.txt"

      # true positives 
      comm -12 /tmp/set_hypothesis_location.txt /tmp/set_reference_location.txt > "${WORK_DIR}/$HYPOTHESIS_FILENAME-tp.txt"


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
      
      # write evaluation result
      printf '"%s";"%s";%s;%s;%s;%s;%s;%s\n' "${tool}" "${name}" "${n_hypothesis}" "${n_reference}" "${n_true_positive}" "${precision}" "${recall}" "${fscore}" >> "$EVALUATION_RESULT"

      echo "======================    ==================================="
  }
  # --------------------------------------------------------------------------
  eval_corpus "location" \<placeName\>.*?\<\/placeName\>
done < "$HYPOTHESIS_FILES"
# ----------------------------------------------------------------------------
# order evaluation result
sort -t";" -k8 -n -o "$EVALUATION_RESULT" "$EVALUATION_RESULT"
# ----------------------------------------------------------------------------
# append header
sed -i '1i "tool";"type";"retrived";"relevant";"true_positive";"precision";"recall";"f-score"' "$EVALUATION_RESULT"
# ----------------------------------------------------------------------------
cat "$EVALUATION_RESULT"
