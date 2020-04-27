#!/usr/bin/env python3

# Get statistics for tokenized text with blank lines separating documents,
# one sentence per line, and space-separated tokens.

import sys

from collections import Counter


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('file', nargs='+')
    return ap


def print_stats(name, stats):
    print('\t'.join([name] +
                    ['{}:{}'.format(k,v) for k,v in sorted(stats.items())])
    )

def tokenized_stats(fn, options):
    stats = Counter()
    text_seen = False
    with open(fn) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip()
            if l.isspace() or not l:
                if text_seen:
                    stats['documents'] += 1
                text_seen = False
            else:
                stats['sentences'] += 1
                stats['tokens'] += len(l.split())
                text_seen = True
    return stats


def main(argv):
    args = argparser().parse_args(argv[1:])
    totals = Counter()
    for fn in args.file:
        stats = tokenized_stats(fn, args)
        print_stats(fn, stats)
        totals = totals + stats
    print_stats('TOTAL', totals)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
