#!/bin/bash

# Sample given ratio of sentences for given language.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$PIPELINE_DIR/common.sh"

mkdir -p "$SAMPLED_TEXT_DIR"

if [ -s "$SAMPLED_TEXT_PATH" ]; then
    echo "$SCRIPT: $SAMPLED_TEXT_PATH exists, skipping sampling." >&2
    exit 0
fi

count=$(find "$DOC_FILTERED_DIR" -type f | wc -l | perl -pe 's/\s//g')

if [ $count -eq 0 ]; then
    error_exit "no files in $DOC_FILTERED_DIR"
else
    echo "$SCRIPT: processing $count files in $DOC_FILTERED_DIR"
fi

# Grab total number of sentences, determine sampling probability to
# get approximately targeted number of sentences.
total=$(find "$DOC_FILTERED_DIR" -type f | sort | xargs cat \
	    | egrep -v '^[[:space:]]*$' | wc -l | perl -pe 's/\s//g')

ratio=$(python3 -c "print(min(1.0, $SAMPLED_SENTENCE_NUM/$total))")

echo "$SCRIPT: sampling $ratio of sentences (total $total, target $SAMPLED_SENTENCE_NUM)" >&2

find "$DOC_FILTERED_DIR" -type f | sort | xargs cat \
    | egrep -v '^[[:space:]]*$' \
    | perl -pe '$_ = "" unless(rand()<'"$ratio"')' \
	   > "$SAMPLED_TEXT_PATH"

result=$(wc -l < "$SAMPLED_TEXT_PATH" | perl -pe 's/\s//g')

echo "$SCRIPT sampled $result sentences (target $SAMPLED_SENTENCE_NUM)"
