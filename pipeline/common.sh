#!/bin/bash

# Shared settings and functionality for pipeline scripts

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 LC" >&2
    echo "    where LC is a two-character language code (e.g. \"en\")" >&2
    exit 1
fi

LC="$1"

error_exit () {
    echo "$SCRIPT: error: $1" >&2
    exit 1
}

relative_path () {
    python3 -c "import os.path; print(os.path.relpath('$1', '$2'))"
}

pwd_relative_path () {
    relative_path "$1" `pwd`
}

SCRIPT=$(pwd_relative_path "$0")
BASE_DIR=$(pwd_relative_path "$PIPELINE_DIR/..")
LANGUAGE_DATA_DIR=$(pwd_relative_path "$BASE_DIR/languages")
SCRIPT_DIR=$(pwd_relative_path "$BASE_DIR/scripts")
DATA_DIR=$(pwd_relative_path "$BASE_DIR/data")
CONFIG_DIR=$(pwd_relative_path "$BASE_DIR/config")

if [ ! -e "$LANGUAGE_DATA_DIR/$LC.json" ]; then
    error_exit "Unknown language $LC (missing $LANGUAGE_DATA_DIR/$LC.json)"
fi

get_language_attribute () {
    python3 "$SCRIPT_DIR/getvalue.py" "$LANGUAGE_DATA_DIR/$1.json" "$2"
}

WIKI_DUMP_URL=$(get_language_attribute "$LC" "wiki-dump")
WIKI_DUMP_DIR="$DATA_DIR/$LC/wikipedia-dump"
WIKI_DUMP_PATH="$WIKI_DUMP_DIR/$(basename $WIKI_DUMP_URL)"

WIKIEXTRACTOR="$BASE_DIR/wikiextractor/WikiExtractor.py"
WIKI_TEXT_DIR="$DATA_DIR/$LC/wikipedia-texts"

UDPIPE_MODEL_URL=$(get_language_attribute "$LC" "udpipe-model")
UDPIPE_MODEL_DIR="$DATA_DIR/$LC/udpipe-model"
UDPIPE_MODEL_PATH="$UDPIPE_MODEL_DIR/$(basename $UDPIPE_MODEL_URL)"

TOKENIZER="$SCRIPT_DIR/udtokenize.py"
TOKENIZED_TEXT_DIR="$DATA_DIR/$LC/tokenized-texts"

DOC_FILTER="$SCRIPT_DIR/filterdocs.py"
DOC_FILTER_WORD_CHARS=$(get_language_attribute "$LC" "word-chars")
DOC_FILTERED_DIR="$DATA_DIR/$LC/filtered-texts"
source "$CONFIG_DIR/filter.sh"

SAMPLED_TEXT_DIR="$DATA_DIR/$LC/sampled-texts"
SAMPLED_TEXT_PATH="$SAMPLED_TEXT_DIR/sampled-sentences.txt"
SAMPLED_SENTENCE_NUM=10000000

BASICTOKENIZE="$SCRIPT_DIR/basictokenize.py"
TOKENIZED_SAMPLE_DIR="$DATA_DIR/$LC/tokenized-samples"
TOKENIZED_SAMPLE_PATH="$TOKENIZED_SAMPLE_DIR/tokenized-sample-cased.txt"

SENTENCEPIECE_MODEL_DIR="$DATA_DIR/$LC/sentencepiece"
SENTENCEPIECE_MODEL_PATH="$SENTENCEPIECE_MODEL_DIR/cased"
SENTENCEPIECE_VOCAB_PATH="$SENTENCEPIECE_MODEL_PATH.vocab"
SENTENCEPIECE="$SCRIPT_DIR/spmtrain.py"
source "$CONFIG_DIR/sentencepiece.sh"

WORDPIECE_VOCAB_DIR="$DATA_DIR/$LC/wordpiece/cased"
WORDPIECE_VOCAB_PATH="$WORDPIECE_VOCAB_DIR/vocab.txt"
SENT2WORDPIECE=$(pwd_relative_path "$BASE_DIR/sent2wordpiece/sent2wordpiece.py")
SENT2WORDPIECE_PARAMS=""

TFRECORD_DIR_128="$DATA_DIR/$LC/tfrecords/seq-128"
TFRECORD_DIR_512="$DATA_DIR/$LC/tfrecords/seq-512"
CREATE_TFRECORD="$BASE_DIR/bert/create_pretraining_data.py"
source "$CONFIG_DIR/tfrecord.sh"

MD5SUM_DIR="$DATA_DIR/$LC/md5sums"
