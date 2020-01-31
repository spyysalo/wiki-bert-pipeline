#!/bin/bash

# Tokenize texts for given language.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$PIPELINE_DIR/common.sh"

count=$(find "$WIKI_TEXT_DIR" -type f | wc -l | perl -pe 's/\s//g')

if [ $count -eq 0 ]; then
    error_exit "no files in $WIKI_TEXT_DIR"
else
    echo "$SCRIPT: processing $count files in $WIKI_TEXT_DIR"
fi

find "$WIKI_TEXT_DIR" -type f | sort | while read f; do
    relpath=$(relative_path "$f" "$WIKI_TEXT_DIR")
    reldir=$(dirname "$relpath")
    outdir="$TOKENIZED_TEXT_DIR/$reldir"
    outbase=$(echo $(basename "$f") | perl -pe 's/\..*//')
    outpath=$(pwd_relative_path "$outdir/$outbase")
    mkdir -p "$outdir"
    if [ -s "$outpath" ]; then
	echo "$SCRIPT: $outpath exists, skipping $f ." >&2
    else
	echo "$SCRIPT: tokenizing $f to $outpath ..." >&2
	python3 "$TOKENIZER" "$UDPIPE_MODEL_PATH" "$f" \
		> "$outpath"
    fi
done
