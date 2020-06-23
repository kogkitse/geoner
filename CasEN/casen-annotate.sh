#!/bin/bash

if [ $# -ne 1 ]; then
	echo "illegal number of parameters, use e.g."
	echo "./casen-annotate.sh INPUT_FILE"
	exit 1
fi

INPUT="$1"


HYPOTHESIS_FILENAME=$(basename "$INPUT")
HYPOTHESIS_EXTENSION="${HYPOTHESIS_FILENAME##*.}"
HYPOTHESIS_FILENAME="${HYPOTHESIS_FILENAME%.*}"

if [ ! -f "$INPUT" ]; then
	echo "File $INPUT does not exit"
	exit 1
fi

DIR=$(pwd)

UNITEX_BIN="/home/eleni/Unitex-GramLab-3.1beta/App/UnitexToolLogger"
CASSEN_LANG="/home/eleni/workspace/Unitex-GramLab/Unitex/French"
CASSEN_CORPUS="$CASSEN_LANG/Corpus"
CASSEN_DICOS="/home/eleni/Unitex-GramLab-3.1beta/French/Dela"

CASSEN_INPUT="cassen-input"
CASSEN_OUTPUT="cassen-hypothesis"

# prepare input
cat "$INPUT" | sed 's|$| {S}|g' > "$CASSEN_CORPUS/$CASSEN_INPUT.txt"

# prepare cassen directory
mkdir -p "$CASSEN_CORPUS/$CASSEN_INPUT""_snt" 

# normalize input
$UNITEX_BIN Normalize "$CASSEN_CORPUS/$CASSEN_INPUT.txt" "-r$CASSEN_LANG/Norm.txt" "--output_offsets=$CASSEN_CORPUS/$CASSEN_INPUT""_snt/normalize.out.offsets" -qutf8-no-bom

# tokenize input
$UNITEX_BIN Tokenize "$CASSEN_CORPUS/$CASSEN_INPUT.snt" "-a$CASSEN_LANG/Alphabet.txt" -qutf8-no-bom

# apply dictionnaires
$UNITEX_BIN Dico "-t$CASSEN_CORPUS/$CASSEN_INPUT.snt" "-a$CASSEN_LANG/Alphabet.txt" "-m$CASSEN_DICOS/dela-fr-public.bin" "$CASSEN_DICOS/Dnum.fst2" "$CASSEN_DICOS/ajouts80jours.bin" "$CASSEN_DICOS/motsGramf-.bin" "$CASSEN_DICOS/profession.bin" "$CASSEN_DICOS/Papes.fst2" "$CASSEN_DICOS/Dnum-ch.fst2" "$CASSEN_DICOS/dela-fr-public.bin" "$CASSEN_DICOS/NPr+.fst2" "$CASSEN_DICOS/tagger_data_cat.bin" "$CASSEN_DICOS/CR.fst2" "$CASSEN_DICOS/Suffixes+.fst2" "$CASSEN_DICOS/Prolex-Unitex_1_2.bin" "$CASSEN_DICOS/prenom-c.bin" "$CASSEN_DICOS/tagger_data_morph.bin" "$CASSEN_DICOS/Extrait-DelquefM2.bin" "$CASSEN_DICOS/RomNum.bin" "$CASSEN_DICOS/Elements.fst2" "$CASSEN_DICOS/Dnum-ch-fst-text.fst2" "$CASSEN_DICOS/Delaf.bin" "$CASSEN_DICOS/prenom-s.bin" "$CASSEN_LANG/Dela/CasEN_Dico.bin" "$CASSEN_LANG/Dela/Prolex-Unitex-BestOf_2_2_fra.bin" "$CASSEN_LANG/Dela/CasEN_Ambiguites-.bin" -qutf8-no-bom

# run cassys
$UNITEX_BIN Cassys "-a$CASSEN_LANG/Alphabet.txt" "-t$CASSEN_CORPUS/$CASSEN_INPUT.snt" "-l$CASSEN_LANG/Cassys/CasEN_analyse_GEO.csc" "-w$CASSEN_DICOS/dela-fr-public.bin" -v "-r$CASSEN_LANG/Graphs/" "--input_offsets=$CASSEN_CORPUS/$CASSEN_INPUT""_snt/normalize.out.offsets" -qutf8-no-bom

# extract output
$UNITEX_BIN Concord "$CASSEN_CORPUS/$CASSEN_INPUT""_snt/concord.ind" "-m$CASSEN_CORPUS/$CASSEN_OUTPUT-raw.txt" -qutf8-no-bom

# create output
./casen-clean-output.sh "$CASSEN_CORPUS/$CASSEN_OUTPUT-raw.txt" > "./output_casen/hypo_CasEN_$HYPOTHESIS_FILENAME.txt"

