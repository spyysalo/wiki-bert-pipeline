#!/bin/bash

# Create TFRecords with given vocabulary and sequence length.

# NOTE: replace instances of "DOC_FILTERED" with "TOKENIZED_TEXT" in this
# script to generate records for all texts (instead of filtered).

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$PIPELINE_DIR/common.sh"

count=$(find "$DOC_FILTERED_DIR" -type f | wc -l | perl -pe 's/\s//g')

if [ $count -eq 0 ]; then
    error_exit "no files in $DOC_FILTERED_DIR"
else
    echo "$SCRIPT: processing $count files in $DOC_FILTERED_DIR"
fi

for seq_len in 128 512; do
    find "$DOC_FILTERED_DIR" -type f | sort | while read f; do
	relpath=$(relative_path "$f" "$DOC_FILTERED_DIR")
	reldir=$(dirname "$relpath")
	if [ $seq_len -eq 128 ]; then
	    outdir="$TFRECORD_DIR_128/$reldir"
	    params="$CREATE_TFRECORD_PARAMS $CREATE_TFRECORD_PARAMS_128"
	elif [ $seq_len -eq 512 ]; then
	    outdir="$TFRECORD_DIR_512/$reldir"
	    params="$CREATE_TFRECORD_PARAMS $CREATE_TFRECORD_PARAMS_512"
	else
	    error_exit "unexpected seq_len $seq_len"
	fi
	outbase=$(echo $(basename "$f") | perl -pe 's/\..*//')
	outpath=$(pwd_relative_path "$outdir/$outbase.tfrecord")
	mkdir -p "$outdir"
	if [ -s "$outpath" ]; then
	    echo "$SCRIPT: $outpath exists, skipping $f ." >&2
	else
	    echo "$SCRIPT: creating TFRecord from $f to $outpath ..." >&2
	    echo "$SCRIPT: running $CREATE_TFRECORD" $params >&2
	    python3 "$CREATE_TFRECORD" $params \
		    --input_file="$f" \
		    --output_file="$outpath"
	fi
    done
done
