#!/bin/bash

# Pipeline driver script.

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 LC" >&2
    echo "    where LC is a two-character language code (e.g. \"en\")" >&2
    exit 1
fi

LC="$1"

set -euo pipefail

# https://stackoverflow.com/a/246128
BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

SCRIPTDIR="$BASEDIR/pipeline"

br=$(basename "$0")
echo $'\n'"---------- $br $LC: START ----------" >&2
echo "           $(date)"$'\n' >&2

for script in $(find "$SCRIPTDIR" -maxdepth 1 -name '[0-9]*.sh' | sort); do
    br=$(basename "$0")
    bs=$(basename "$script")
    echo $'\n'"---------- $br: RUNNING $bs ----------" >&2
    echo "           $(date)"$'\n' >&2
    "$script" "$LC"
    echo $'\n'"---------- $br: COMPLETED $bs ----------" >&2
    echo "           $(date)"$'\n' >&2
done

echo $'\n'"---------- $br: DONE ----------" >&2
echo "           $(date)"$'\n' >&2
