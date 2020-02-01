# BERT Wiki vocabularies

Tools for creating BERT vocabularies based on Wikipedia texts

## Quickstart

Setup

```
git submodule init
git submodule update
pip3 install -r requirements.txt
```

To run the full process for a language with the two-character language
code LC, run

```
./RUN.sh LC
```

(For example, `./RUN.sh fi` for Finnish.)

## Adding new languages

To add support for a new language with the two-character language code
LC, create `metadata/LC.json` and fill in the relevant values for
`word-chars` (sequence of word characters), `wiki-dump` (URL) and
`udpipe-model` (URL). See the existing JSON files in `metadata/`
for examples.

## Limitations

The source texts are extracted from Wikipedia, and the quality of the
generated vocabulary depends on the quantity (and quality) of Wikipedia
text available for the language.

The document filtering heuristics were developed for Indo-European
languages written with (variants of) the Latin alphabet. They are
likely to fail disastrously for other languages. The rest of the
pipeline should work, though, if the filtering is disabled.

The pipeline performs sentence segmentation with UDPipe and is
thus limited to the languages for which a UDPipe model is available.
As of this writing, models are available for 60 languages from
https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-2998 .
