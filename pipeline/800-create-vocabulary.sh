#!/bin/bash

# Create sentencepiece model for given language.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$PIPELINE_DIR/common.sh"

if [ ! -s "$TOKENIZED_SAMPLE_PATH" ]; then
    error_exit "$TOKENIZED_SAMPLE_PATH does not exist"
fi

mkdir -p "$SENTENCEPIECE_MODEL_DIR"

if [ -s "$SENTENCEPIECE_MODEL_PATH" ]; then
    echo "$SCRIPT: $SENTENCEPIECE_MODEL_PATH exists, not recreating." >&2
    exit 0
else
    params="
--input=$TOKENIZED_SAMPLE_PATH
--model_prefix=$SENTENCEPIECE_MODEL_PATH
$SENTENCEPIECE_PARAMS"
    echo "$SCRIPT: running $SENTENCEPIECE" $params >&2
    python3 "$SENTENCEPIECE" $params
fi
