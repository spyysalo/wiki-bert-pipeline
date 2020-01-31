#!/usr/bin/env python3

import sys

from sentencepiece import SentencePieceTrainer


def main(argv):
    SentencePieceTrainer.Train(' '.join(argv[1:]))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
