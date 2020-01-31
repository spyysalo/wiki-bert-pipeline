#!/bin/bash

# Download Wikipedia dump data for given language.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$PIPELINE_DIR/common.sh"

mkdir -p "$WIKI_DUMP_DIR"

if [ -s "$WIKI_DUMP_PATH" ]; then
    echo "$SCRIPT: $WIKI_DUMP_PATH exists, skipping download." >&2
    exit 0
else
    echo "$SCRIPT: downloading $WIKI_DUMP_URL to $WIKI_DUMP_PATH ..." >&2
    wget -O "$WIKI_DUMP_PATH" "$WIKI_DUMP_URL"
fi    
