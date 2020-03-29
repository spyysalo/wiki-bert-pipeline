#!/usr/bin/env python3

import sys
import re
import json
import gzip
import bz2

from collections import Counter
from logging import warning

try:
    from ufal.udpipe import Model, Pipeline
except ImportError:
    print('Failed to import ufal.udpipe. (Try `pip3 install ufal.udpipe`?)',
          file=sys.stderr)
    sys.exit(1)


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
    ap.add_argument('-n', '--no-split', default=False, action='store_true',
                    help='Do not split sentences on separate lines')
    ap.add_argument('-s', '--save-stats', metavar='FILE', default=None)
    ap.add_argument('-q', '--quiet', default=False, action='store_true')
    ap.add_argument('model', help='UDPipe model')
    ap.add_argument('file', nargs='+')
    return ap


def create_model(model_path):
    model = Model.load(model_path)
    pipeline = Pipeline(model, 'tokenize', 'none', 'none', 'horizontal')
    return model, pipeline


def character_count(text):
    return len(list(c for c in text if not c.isspace()))


def token_count(text):
    return len(list(t for t in text.split()))


def sentence_count(text):
    return len(list(s for s in text.split('\n') if s.strip()))


def tokenize_stream(pipeline, f, fn, options):
    stats = Counter()
    for ln, l in enumerate(f, start=1):
        l = l.rstrip('\n')
        if '\x00' in l:
            warning('Removing null bytes from text in {}: {}'.format(fn, l))
            l = l.replace('\x00', '')
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
            t = pipeline.process(l)
            stats['characters'] += character_count(t)
            stats['tokens'] += token_count(t)
            stats['sentences'] += sentence_count(t)
            t = t.rstrip('\n')
            if options.no_split:
                t = t.replace('\n', ' ')
            print(t)
    return stats


def tokenize(pipeline, fn, options):
    if fn.endswith('.gz'):
        with gzip.open(fn, 'rt', encoding=options.encoding) as f:
            return tokenize_stream(pipeline, f, fn, options)
    elif fn.endswith('.bz2'):
        with bz2.open(fn, 'rt', encoding=options.encoding) as f:
            return tokenize_stream(pipeline, f, fn, options)
    else:
        with open(fn) as f:
            return tokenize_stream(pipeline, f, fn, options)


def main(argv):
    args = argparser().parse_args(argv[1:])
    model, pipeline = create_model(args.model)
    totals = Counter()
    for fn in args.file:
        totals += tokenize(pipeline, fn, args)
    if args.save_stats:
        with open(args.save_stats, 'w') as out:
            json.dump(dict(totals.items()), out, indent=4)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
