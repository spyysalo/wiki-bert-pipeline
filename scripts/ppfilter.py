#!/usr/bin/env python3

import sys


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('--min-tokens', default=None, type=int)
    ap.add_argument('--trim-threshold', default=None, type=float)
    ap.add_argument('--threshold', default=10000, type=float)
    ap.add_argument('file', nargs='+')
    return ap


def trim_document(perplexities, sentences, lengths, options):
    assert len(perplexities) == len(sentences)

    threshold, min_tokens = options.trim_threshold, options.min_tokens
    if threshold is None:
        threshold = sys.float_info.max
    if min_tokens is None:
        min_tokens = 0

    start, end = 0, len(sentences)
    while start < len(perplexities) and (
            perplexities[start] > threshold or
            lengths[start] < min_tokens):
        start += 1
    while end > start and (
            perplexities[end-1] > threshold or
            lengths[end-1] < min_tokens):
        end -= 1

    return perplexities[start:end], sentences[start:end], lengths[start:end]


def average_perplexity(perplexities, sentences, lengths, options):
    filtered = []
    for p, s, l in zip(perplexities, sentences, lengths):
        # Only take average for sentences longer than minimum (if any)
        if options.min_tokens is None or l >= options.min_tokens:
            filtered.append(p)
    if not filtered:
        return None
    return sum(filtered)/len(filtered)


def process_document(perplexities, sentences, options):
    assert len(perplexities) == len(sentences)

    lengths = [len(s.split()) for s in sentences]

    perplexities, sentences, lengths = trim_document(
        perplexities, sentences, lengths, options)
    if not sentences:
        return 0    # empty after trimming

    avg = average_perplexity(perplexities, sentences, lengths, options)
    if avg is None or avg > options.threshold:
        return 0
    
    print('\n'.join(sentences))
    print()
    return 1


def process_file(fn, options):
    perplexities, sentences = [], []
    output, total = 0, 0
    with open(fn) as f:
        for ln, l in enumerate(f, start=1):
            l = l.rstrip('\n')
            if l.isspace() or not l:
                output += process_document(perplexities, sentences, options)
                total += 1
                perplexities, sentences = [], []
                continue
            try:
                perplexity, sentence = l.split('\t', 1)
                perplexity = float(perplexity)
            except:
                raise ValueError('Failed to parse line {} in {}: {}'.format(
                    ln, fn, l))
            perplexities.append(perplexity)
            sentences.append(sentence)
    print('Output {}/{} ({:.1%}) for {}'.format(
        output, total, output/total, fn), file=sys.stderr)


def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.file:
        process_file(fn, args)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
