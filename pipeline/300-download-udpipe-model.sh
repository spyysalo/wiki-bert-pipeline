#!/bin/bash

# Download UDPipe model for given language.

PIPELINE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$PIPELINE_DIR/common.sh"

mkdir -p "$UDPIPE_MODEL_DIR"

if [ -s "$UDPIPE_MODEL_PATH" ]; then
    echo "$SCRIPT: $UDPIPE_MODEL_PATH exists, skipping download." >&2
    exit 0
else
    echo "$SCRIPT: downloading $UDPIPE_MODEL_URL to $UDPIPE_MODEL_PATH ..." >&2
    wget -O "$UDPIPE_MODEL_PATH" "$UDPIPE_MODEL_URL"
fi    
