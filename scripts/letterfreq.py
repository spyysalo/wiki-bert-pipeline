#!/usr/bin/env python3

# Get frequencies of letter characters in text.

import sys
import re

from collections import Counter


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser(description='Get letter frequencies.')
    ap.add_argument('--ignore', default=None,
                    help='ignore given characters')
    ap.add_argument('--lower', default=False, action='store_true',
                    help='lowercase input')
    ap.add_argument('file', nargs='+')
    return ap


def main(argv):
    args = argparser().parse_args(argv[1:])
    ignore = '' if args.ignore is None else args.ignore
    letter_re = re.compile(r'[^\W\d_'+ignore+r']')
    counts = Counter()
    for fn in args.file:
        with open(fn) as f:
            for ln, l in enumerate(f, start=1):
                l = l.rstrip('\n')
                if args.lower:
                    l = l.lower()
                counts.update(letter_re.findall(l))
    total = sum(counts.values())
    for k, v in sorted(counts.items(), key=lambda i: -i[1]):
        print('{}\t{}\t({:.2%})'.format(v, k, v/total))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
