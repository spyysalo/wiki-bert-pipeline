#!/usr/bin/env python3

# Calculate perplexity for sentence-split, tokenized text using
# kenln language model

import sys
import gzip

import kenlm


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('--encoding', default='utf-8')
    ap.add_argument('model')
    ap.add_argument('file', nargs='+')
    return ap


def process_stream(f, fn, model, options):
    for ln, l in enumerate(f, start=1):
        l = l.rstrip('\n')
        if l.isspace() or not l:
            print()
        else:
            print('{}\t{}'.format(model.perplexity(l), l))


def process(fn, model, options):
    if fn.endswith('.gz'):
        with gzip.open(fn, mode='rt', encoding=options.encoding) as f:
            process_stream(f, fn, model, options)
    else:
        with open(fn) as f:
            process_stream(f, fn, model, options)


def main(argv):
    args = argparser().parse_args(argv[1:])
    model = kenlm.Model(args.model)
    for fn in args.file:
        process(fn, model, args)
        return 0

    
if __name__ == '__main__':
    sys.exit(main(sys.argv))

