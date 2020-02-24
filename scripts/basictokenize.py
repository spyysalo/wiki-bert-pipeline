#!/usr/bin/env python3

import sys
import re
import bz2

from bert.tokenization import BasicTokenizer


# Match WikiExtractor document start and end tags
DOC_START_TAG_RE = re.compile(r'^<doc\s+id=.*>$')
DOC_END_TAG_RE = re.compile(r'^</doc>$')


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-b', '--keep-blank', default=False, action='store_true',
                    help='Include blank lines in output')
    ap.add_argument('-d', '--document-tags', default=False, action='store_true',
                    help='Include document start/end tags in output')
    ap.add_argument('-e', '--encoding', default='utf-8')
    ap.add_argument('--uncased', default=False, action='store_true',
                    help='Lowercase and strip accents (for uncased model)')
    ap.add_argument('file', nargs='+')
    return ap


def tokenize_stream(tokenizer, f, fn, options):
    for ln, l in enumerate(f, start=1):
        l = l.rstrip('\n')
        start_m = DOC_START_TAG_RE.match(l)
        end_m = DOC_END_TAG_RE.match(l)
        if l.isspace() or not l:
            if options.keep_blank:
                print(l)
        elif start_m or end_m:
            if options.document_tags:
                print(l)
            elif end_m:
                print()    # Empty line as doc boundary
        else:
            print(' '.join(tokenizer.tokenize(l)))


def basic_tokenize(tokenizer, fn, options):
    if fn.endswith('.bz2'):
        with bz2.open(fn, 'rt', encoding=options.encoding) as f:
            tokenize_stream(tokenizer, f, fn, options)
    else:
        with open(fn) as f:
            tokenize_stream(tokenizer, f, fn, options)


def main(argv):
    args = argparser().parse_args(argv[1:])
    tokenizer = BasicTokenizer(do_lower_case=args.uncased)
    for fn in args.file:
        basic_tokenize(tokenizer, fn, args)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
