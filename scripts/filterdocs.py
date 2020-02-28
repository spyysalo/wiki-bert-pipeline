#!/usr/bin/env python3

# Filter blank line-separated sentence-per-line text documents.

import sys
import os
import re
import unicodedata

from string import punctuation
from collections import Counter

try:
    from langdetect import detect, DetectorFactory
    # Make langdetect deterministic
    DetectorFactory.seed = 0
except ImportError:
    print('failed to import langdetect, language detection unavailable.',
          file=sys.stderr)
    detect = None


# Regex definition for e.g. --min-words option
WORD_RE = None    # see compile_regular_expressions()

# Regex definition for --foreign-ratio option
FOREIGN_LETTER = None    # see compile_regular_expressions()


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser(description='Filter documents.')
    ap.add_argument('-a', '--avg-len', default=None, type=int,
                    help='minimum average sentence length (lowercase words)')
    ap.add_argument('-d', '--digit-ratio', default=None, type=float,
                    help='maximum ratio of digit characters')
    ap.add_argument('-F', '--foreign-ratio', default=None, type=float,
                    help='maximum ratio of non-word alphabetic characters')
    ap.add_argument('-i', '--invert', default=False, action='store_true',
                    help='invert filter criteria')
    ap.add_argument('-l', '--langdetect', metavar='LANG', default=None,
                    help='run langdetect to filter to LANG')
    ap.add_argument('-L', '--limit', default=None, type=int,
                    help='limit number of documents to process')
    ap.add_argument('--language', default=None,
                    help='language code')
    ap.add_argument('-n', '--no-word-ratio', default=None, type=float,
                    help='maximum ratio of lines without word tokens')
    ap.add_argument('-p', '--punct-ratio', default=None, type=float,
                    help='maximum ratio of punctuation characters')
    ap.add_argument('-s', '--min-sents', default=None, type=int,
                    help='minimum number of sentences')
    ap.add_argument('-S', '--max-sents', default=None, type=int,
                    help='maximum number of sentences')
    ap.add_argument('-t', '--min-toks', default=None, type=int,
                    help='minimum number of tokens')
    ap.add_argument('-T', '--max-toks', default=None, type=int,
                    help='maximum number of tokens')
    ap.add_argument('-u', '--upper-ratio', default=None, type=float,
                    help='maximum ratio of uppercase characters')
    ap.add_argument('-w', '--min-words', default=None, type=int,
                    help='minimum number of words')
    ap.add_argument('-W', '--word-chars', default=None,
                    help='characters allowed as part of words')
    ap.add_argument('file', nargs='+')
    return ap


def num_toks(sentences):
    return sum(len(s.split()) for s in sentences)


def num_words(sentences):
    return sum(len(WORD_RE.findall(s)) for s in sentences)


def foreign_ratio(sentences):
    return sum(len(FOREIGN_LETTER.findall(s)) for s in sentences)/char_count(sentences)


def avg_len(sentences):
    return num_words(sentences) / len(sentences)


def char_count(sentences):
    return sum(len(s) for s in sentences)


def uppercase_ratio(sentences):
    return sum(c.isupper() for s in sentences for c in s)/char_count(sentences)


def digit_ratio(sentences):
    return sum(c.isdigit() for s in sentences for c in s)/char_count(sentences)


def no_word_ratio(sentences):
    return sum(1 for s in sentences if len(WORD_RE.findall(s)) == 0)/len(sentences)


def punctuation_ratio(sentences):
    punct = set(punctuation)
    return sum(c in punct for s in sentences for c in s)/char_count(sentences)


def detect_lang(sentences):
    if detect is None:
        raise ImportError('langdetect module not available')
    try:
        return detect(' '.join(sentences))
    except:
        return None


def filter_sentences(sentences, options):
    if options.avg_len is not None and avg_len(sentences) < options.avg_len:
        return 'avg-len'
    if options.min_sents is not None and len(sentences) < options.min_sents:
        return 'min-sents'
    if options.max_sents is not None and len(sentences) > options.max_sents:
        return 'max-sents'
    if options.min_toks is not None and num_toks(sentences) < options.min_toks:
        return 'min-toks'
    if options.max_toks is not None and num_toks(sentences) > options.max_toks:
        return 'max-toks'
    if (options.no_word_ratio is not None and
        no_word_ratio(sentences) > options.no_word_ratio):
        return 'no-word-ratio'
    if (options.punct_ratio is not None and
        punctuation_ratio(sentences) > options.punct_ratio):
        return 'punct-ratio'
    if (options.upper_ratio is not None and
        uppercase_ratio(sentences) > options.upper_ratio):
        return 'upper-ratio'
    if (options.digit_ratio is not None and
        digit_ratio(sentences) > options.digit_ratio):
        return 'digit-ratio'
    if (options.foreign_ratio is not None and
        foreign_ratio(sentences) > options.foreign_ratio):
        return 'foreign-ratio'
    if (options.min_words is not None and
        num_words(sentences) < options.min_words):
        return 'min-words'
    if (options.langdetect is not None and
        detect_lang(sentences) != options.langdetect):
        return 'langdetect'
    return None


def report_stats(name, stats, out=sys.stderr):
    stats = stats.copy()
    docs, output = stats.pop('total-docs'), stats.pop('output-docs')
    for k, v in sorted(stats.items()):
        print('{}:\t{}\t{} ({:.1%})'.format(
            name, k, v, v/docs), file=sys.stderr, flush=True)
    print('{}: output {}/{} documents ({:.1%})'.format(
        name, output, docs, output/docs), file=sys.stderr, flush=True)
    pass


def process_document(sentences, stats, options):
    fail = filter_sentences(sentences, options)
    if fail is None:
        result = 'pass-all'
        skip = False
    else:
        result = 'fail-{}'.format(fail)
        skip = True
    stats[result] += 1
    if options.invert:
        skip = not skip
    if skip:
        return 0
    else:
        for s in sentences:
            print(s)
        if sentences:
            print()
        return 1


def process(fn, options):
    stats = Counter()
    total_count, output_count = 0, 0
    with open(fn) as f:
        sentences = []
        for ln, l in enumerate(f, start=1):
            l = l.rstrip()
            if l and not l.isspace():
                sentences.append(l)
            else:
                if sentences:
                    output_count += process_document(sentences, stats, options)
                    total_count += 1
                sentences = []
                if options.limit is not None and total_count >= options.limit:
                    break
            if ln % 10000 == 0:
                print('processed {} ...'.format(ln), file=sys.stderr)
        if sentences:
            output_count += process_document(sentences, stats, options)
            total_count += 1
    stats['total-docs'] = total_count
    stats['output-docs'] = output_count
    report_stats(os.path.basename(fn), stats)
    return stats


def japanese_letters():
    ranges = [
        (0x3040, 0x309F),    # Hiragana
        (0x30A0, 0x30FF),    # Katakana
        (0x4E00, 0x9FAF),    # Common and uncommon kanji
        (0x3400, 0x4DBF),    # Rare kanji
    ]
    letters = []
    for start, end in ranges:
        for i in range(start, end+1):
            if unicodedata.category(chr(i)).startswith('L'):
                letters.append(chr(i))
    letters.extend('abcdefghijklmnopqrstuvwxyz')
    return ''.join(letters)


def compile_regular_expressions(options):
    global WORD_RE, FOREIGN_LETTER

    if options.word_chars == 'ja':
        # Special case for Japanese; UD Japanese tokenization is
        # particularly aggressive about splitting up words, so
        # only require a single character length for "word"
        alpha = japanese_letters()
        w_len = 1
    elif options.word_chars:
        alpha = options.word_chars
        w_len = 2
    else:
        print('Warning: --word-chars not given, using [a-z]', file=sys.stderr)
        alpha = 'abcdefghijklmnopqrstuvwxyz'
        w_len = 2
    upper = ''.join([a.upper() for a in alpha if a.upper() not in alpha])

    # Heuristic for "regular" word: a minimum number of word characters,
    # optionally with an initial uppercase character (if ones exist
    # for the language).
    w = str(w_len)
    if upper:
        WORD_RE = re.compile(r'\b['+upper+r']?['+alpha+r']{'+w+r',}\b')
    else:
        WORD_RE = re.compile(r'\b['+alpha+r']{'+w+r'}\b')

    # Unicode letter that is not part of the alphabet
    # (https://stackoverflow.com/a/6314634)
    FOREIGN_LETTER = re.compile(r'[^\W\d_'+alpha+upper+r']')


def main(argv):
    args = argparser().parse_args(argv[1:])
    compile_regular_expressions(args)
    totals = Counter()
    for fn in args.file:
        print('processing {} ...'.format(os.path.basename(fn)),
              file=sys.stderr)
        stats = process(fn, args)
        totals.update(stats)
        print('completed {}.'.format(os.path.basename(fn)),
              file=sys.stderr)
    if len(args.file) > 1:
        report_stats('TOTAL', totals)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
