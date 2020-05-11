#!/usr/bin/env python3

# Get statistics for tokenized text with blank lines separating documents,
# one sentence per line, and space-separated tokens.

import sys
import math

from collections import Counter


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-H', '--human-readable', default=False,
                    action='store_true')
    ap.add_argument('-l', '--no-labels', default=False, action='store_true')
    ap.add_argument('-s', '--no-space', default=False, action='store_true')
    ap.add_argument('file', nargs='+')
    return ap


# adapted from https://stackoverflow.com/a/3155023
def human_readable(i):
    names = ['', 'K', 'M', 'B', 'T']
    n = math.floor(0 if i == 0 else math.log10(abs(i))/3)
    idx = max(0, min(len(names)-1, int(n)))
    d = float(i) / 10**(3*idx)
    if len(str(i)) < 2 or len('{:.0f}'.format(d)) > 1:
        s = '{:.0f}'.format(d)
    else:
        s = '{:.1f}'.format(d)
    return '{}{}'.format(s, names[idx])


def print_stats(name, stats, options):
    formatted = []
    for (i, k), v in sorted(stats.items()):
        if options.human_readable:
            v = human_readable(v)
        if options.no_labels:
            formatted.append('{}'.format(v))
        else:
            formatted.append('{}:{}'.format(k, v))
    print('\t'.join([name] + formatted))


def tokenized_stats(fn, options):
    stats = Counter()
    text_seen = False
    with open(fn) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip()
            if l.isspace() or not l:
                if text_seen:
                    stats[(0, 'documents')] += 1
                text_seen = False
            else:
                stats[(1, 'sentences')] += 1
                tokens = l.split()
                stats[(2, 'tokens')] += len(tokens)
                if options.no_space:
                    stats[(3, 'chars')] += sum(len(t) for t in tokens)
                else:
                    stats[(3, 'chars')] += len(l)
                text_seen = True
    return stats


def main(argv):
    args = argparser().parse_args(argv[1:])
    totals = Counter()
    for fn in args.file:
        stats = tokenized_stats(fn, args)
        print_stats(fn, stats, args)
        totals = totals + stats
    print_stats('TOTAL', totals, args)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
