#!/bin/bash

# Create sentencepiece model for given language.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$PIPELINE_DIR/common.sh"

if [ ! -s "$SAMPLED_TEXT_PATH" ]; then
    error_exit "$SAMPLED_TEXT_PATH does not exist"
fi

mkdir -p "$SENTENCEPIECE_MODEL_DIR"

if [ -s "$SENTENCEPIECE_MODEL_PATH" ]; then
    echo "$SCRIPT: $SENTENCEPIECE_MODEL_PATH exists, not recreating." >&2
    exit 0
else
    echo "$SCRIPT: running $SENTENCEPIECE" $SENTENCEPIECE_PARAMS >&2
    python3 "$SENTENCEPIECE" $SENTENCEPIECE_PARAMS
fi
