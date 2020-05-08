#!/usr/bin/env python3

import sys
import re

from collections import Counter


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-t', '--threshold', type=float, default=0.0001,
                    help='Relative frequency cutoff')
    ap.add_argument('file', nargs='+')
    return ap


def count_alpha(fn, options):
    counts = Counter()
    with open(fn) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip()
            for c in l.lower():
                if c.isalpha():
                    counts[c] += 1
    return counts


def main(argv):
    args = argparser().parse_args(argv[1:])
    totals = Counter()
    for fn in args.file:
        counts = count_alpha(fn, args)
        totals.update(counts)
    total = sum(totals.values())
    for k, v in sorted(totals.items(), key=lambda i: i[1], reverse=True):
        print('{}\t{}\t{}\t({:.4%})'.format(
            v/total > args.threshold, k, v, v/total))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
