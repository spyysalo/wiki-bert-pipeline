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
METADATA_DIR=$(pwd_relative_path "$BASE_DIR/metadata")
SCRIPT_DIR=$(pwd_relative_path "$BASE_DIR/scripts")
DATA_DIR=$(pwd_relative_path "$BASE_DIR/data")

get_config_value () {
    python3 "$SCRIPT_DIR/getvalue.py" "$METADATA_DIR/$1.json" "$2"
}

WIKI_DUMP_URL=$(get_config_value "$LC" "wiki-dump")
WIKI_DUMP_DIR="$DATA_DIR/$LC/wikipedia-dump"
WIKI_DUMP_PATH="$WIKI_DUMP_DIR/$(basename $WIKI_DUMP_URL)"

WIKIEXTRACTOR="$BASE_DIR/wikiextractor/WikiExtractor.py"
WIKI_TEXT_DIR="$DATA_DIR/$LC/wikipedia-texts"

UDPIPE_MODEL_URL=$(get_config_value "$LC" "udpipe-model")
UDPIPE_MODEL_DIR="$DATA_DIR/$LC/udpipe-model"
UDPIPE_MODEL_PATH="$UDPIPE_MODEL_DIR/$(basename $UDPIPE_MODEL_URL)"

TOKENIZER="$SCRIPT_DIR/udtokenize.py"
TOKENIZED_TEXT_DIR="$DATA_DIR/$LC/tokenized-texts"

DOC_FILTER="$SCRIPT_DIR/filterdocs.py"
DOC_FILTER_WORD_CHARS=$(get_config_value "$LC" "word-chars")
DOC_FILTERED_DIR="$DATA_DIR/$LC/filtered-texts"
DOC_FILTER_PARAMS="
--min-sents 3
--max-sents 1000
--avg-len 5
--upper-ratio 0.1
--no-word-ratio 0.2
--punct-ratio 0.05
--digit-ratio 0.05
--min-toks 20
--max-toks 10000
--min-words 30
--foreign-ratio 0.01
--word-chars $DOC_FILTER_WORD_CHARS
--langdetect $LC
"

SAMPLED_TEXT_DIR="$DATA_DIR/$LC/sampled-texts"
SAMPLED_TEXT_PATH="$SAMPLED_TEXT_DIR/sampled-sentences.txt"
SAMPLED_SENTENCE_NUM=10000

BASICTOKENIZE="$SCRIPT_DIR/basictokenize.py"
TOKENIZED_SAMPLE_DIR="$DATA_DIR/$LC/tokenized-samples"
TOKENIZED_SAMPLE_PATH="$TOKENIZED_SAMPLE_DIR/tokenized-sample-cased.txt"

SENTENCEPIECE_MODEL_DIR="$DATA_DIR/$LC/sentencepiece"
SENTENCEPIECE_MODEL_PATH="$SENTENCEPIECE_MODEL_DIR/model"
SENTENCEPIECE="$SCRIPT_DIR/spmtrain.py"
SENTENCEPIECE_PARAMS="
--model_prefix=$SENTENCEPIECE_MODEL_PATH
--vocab_size=20000
--input_sentence_size=100000000
--character_coverage=0.9999
--model_type=bpe
--input=$SAMPLED_TEXT_PATH
"
