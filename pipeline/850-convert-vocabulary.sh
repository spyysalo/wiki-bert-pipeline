#!/bin/bash

# Convert sentencepiece to wordpiece vocabulary.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$PIPELINE_DIR/common.sh"

if [ ! -s $SENTENCEPIECE_VOCAB_PATH ]; then
    error_exit "$SENTENCEPIECE_VOCAB_PATH does not exist"
fi

mkdir -p "$WORDPIECE_VOCAB_DIR"

if [ -s "$WORDPIECE_VOCAB_PATH" ]; then
    echo "$SCRIPT: $WORDPIECE_VOCAB_PATH exists, not recreating." >&2
    exit 0
else
    echo "$SCRIPT: running $SENT2WORDPIECE" $SENT2WORDPIECE_PARAMS >&2
    python3 "$SENT2WORDPIECE" $SENT2WORDPIECE_PARAMS \
	    "$SENTENCEPIECE_VOCAB_PATH" > $WORDPIECE_VOCAB_PATH
fi

