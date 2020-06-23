#!/bin/bash

if [ $# -ne 1 ]; then
	echo "illegal number of parameters, use e.g."
	echo "./casen-clean-output.sh INPUT_CASEN_FILE"
	exit 1
fi

INPUT_CASEN_FILE="$1"

#sed '1d'                                                |\
#sed '$ d'                                               |\

dos2unix "$INPUT_CASEN_FILE" 2> /dev/null

cat "$INPUT_CASEN_FILE"                                 |\
sed 's|{S} |\n|g ; s| {S}||g ; s|{S}||g'                |\
sed 's|\\[.+,][^\}]\+||g'                               |\
sed 's|\\{||g ; s|\\,\\}||g'                            |\
sed 's|,\.nombre|,.entity+nombre|g'                     |\
sed 's|,\.ordinal|,.entity+ordinal|g'                   |\
sed 's|,\.baliseXml|,.entity+baliseXml|g'               |\
sed 's|\.entity+\([^+]*\?\)[^}]*\?|.\1|g'               |\
sed 's|{\([^,]*\?\),\.\([^}]*\?\)}|<\2>\1</\2>|g'       |\
sed 's|<baliseXml><\/\?s><\/baliseXml>||g'              |\
sed 's/<\(placeName\|geogName\)[^>]*>/<placeName>/g'        |\
sed 's/<\/\(placeName\|geogName\)[^>]*>/<\/placeName>/g'    |\
sed 's|<nombre>||g ; s|<\/nombre>||g'                       |\
sed 's|[…)\(»«]||g'                                          |\
sed 's|\[||g ; s|]||g'                                     |\
tr '\n' ' '   											|\
sed 's/\.\s*\(\w\|<\)/\.\n\1/g'|\
sed 's/\?\s*\(\w\|<\)/\?\n\1/g'|\
sed 's/!\s*\(\w\|<\)/!\n\1/g'