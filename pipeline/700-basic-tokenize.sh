#!/bin/bash

# Perform BERT basic tokenization.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$PIPELINE_DIR/common.sh"

mkdir -p "$TOKENIZED_SAMPLE_DIR"

if [ -s "$TOKENIZED_SAMPLE_PATH" ]; then
    echo "$SCRIPT: $TOKENIZED_SAMPLE_PATH exists, skipping tokenization." >&2
    exit 0
fi

if [ ! -s "$SAMPLED_TEXT_PATH" ]; then
    error_exit "missing $SAMPLED_TEXT_PATH"
else
    echo "$SCRIPT: performing basic tokenization on $SAMPLED_TEXT_PATH with output to $TOKENIZED_SAMPLE_PATH" >&2
    python3 "$BASICTOKENIZE" "$SAMPLED_TEXT_PATH" > "$TOKENIZED_SAMPLE_PATH"
fi
