#!/usr/bin/env python3

# Get value under given key from JSON file

import sys
import json


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('json')
    ap.add_argument('key')
    return ap
    

def main(argv):
    args = argparser().parse_args(argv[1:])
    try:
        with open(args.json) as f:
            data = f.read()
    except Exception as e:
        print('Error: {}'.format(e), file=sys.stderr)
        return 1
    try:
        data = json.loads(data)
    except Exception as e:
        print('Error: failed to parse {} as JSON: {}'.format(args.json, e),
              file=sys.stderr)
        return 1
    if args.key not in data:
        print('Error: missing key "{}" in {}'.format(args.key, args.json),
              file=sys.stderr)
        return 1
    print(data[args.key])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
