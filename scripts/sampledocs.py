#!/usr/bin/env python3

# Sample documents from text with blank lines as document boundaries

import sys
from random import random, seed


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('--sampled', metavar='FILE', default=None,
                    help='Output sampled to FILE (default stdout)')
    ap.add_argument('--rest', metavar='FILE', default=None,
                    help='Output non-sampled to FILE (not output by default)')
    ap.add_argument('--seed', metavar='INT', default=None, type=int,
                    help='Random seed')
    ap.add_argument('ratio', type=float)
    ap.add_argument('file', nargs='+')
    return ap


def sample_documents(fn, sampled_out, rest_out, options):
    rand = random()
    with open(fn) as f:
        for ln, l in enumerate(f, start=1):
            if rand < options.ratio:
                sampled_out.write(l)
            else:
                rest_out.write(l)
            if l.isspace() or not l:
                rand = random()


class NullOut(object):
    def write(self, *args):
        pass


def main(argv):
    args = argparser().parse_args(argv[1:])
    seed(args.seed)
    if args.sampled is None:
        sampled_out = sys.stdout
    else:
        sampled_out = open(args.sampled, 'w')
    if args.rest is None:
        rest_out = NullOut()
    else:
        rest_out = open(args.rest, 'w')        
    for fn in args.file:
        sample_documents(fn, sampled_out, rest_out, args)
    if args.sampled is not None:
        sampled_out.close()
    if args.rest is not None:
        rest_out.close()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
