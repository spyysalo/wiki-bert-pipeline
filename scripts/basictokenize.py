#!/usr/bin/env python3

import sys

from bert.tokenization import BasicTokenizer
# from tokenizers.pre_tokenizers import BertPreTokenizer


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('--uncased', default=False, action='store_true',
                    help='Lowercase and strip accents (for uncased model)')
    ap.add_argument('file', nargs='+')
    return ap


def basic_tokenize(tokenizer, fn, options):
    with open(fn) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip('\n')
            print(' '.join(tokenizer.tokenize(l)))
            # tokenized = tokenizer.pre_tokenize(l)
            # print(' '.join(t[0] for t in tokenized))


def main(argv):
    args = argparser().parse_args(argv[1:])
    # tokenizer = BertPreTokenizer.new(
    #     strip_accents=args.uncased,
    #     lowercase=args.uncased
    # )
    tokenizer = BasicTokenizer(do_lower_case=args.uncased)
    for fn in args.file:
        basic_tokenize(tokenizer, fn, args)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))