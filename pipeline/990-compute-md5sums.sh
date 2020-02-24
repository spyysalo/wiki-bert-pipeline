#!/bin/bash

# Compute md5sums for selected outputs.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$PIPELINE_DIR/common.sh"

mkdir -p "$MD5SUM_DIR"

outpath="$MD5SUM_DIR/tfrecords-128.md5sum"
if [ -s "$outpath" ]; then
    echo "$SCRIPT: $outpath exists, skipping." >&2
else
    echo "$SCRIPT: computing md5sums for files in $TFRECORD_DIR_128 with output to $outpath ." >&2
    find "$TFRECORD_DIR_128" -name '*.tfrecord' | \
	xargs md5sum > "$outpath"
fi

outpath="$MD5SUM_DIR/tfrecords-512.md5sum"
if [ -s "$outpath" ]; then
    echo "$SCRIPT: $outpath exists, skipping." >&2
else
    echo "$SCRIPT: computing md5sums for files in $TFRECORD_DIR_512 with output to $outpath ." >&2
    find "$TFRECORD_DIR_512" -name '*.tfrecord' | \
	xargs md5sum > "$outpath"
fi
