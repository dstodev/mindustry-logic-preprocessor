#!/usr/bin/env python

import argparse
import sys

from src.preprocessor import Preprocessor


def parse_args():
    '''Parse and return command line arguments.'''
    parser = argparse.ArgumentParser(description='Mindustry Logic Preprocessor')
    parser.add_argument('--infile', '-f', nargs='?', type=argparse.FileType('r'),
                        help='Path to input file', default=sys.stdin)
    parser.add_argument('--outfile', '-o', nargs='?', type=argparse.FileType('w'),
                        help='Path to output file', default=sys.stdout)

    return parser.parse_args()


if __name__ == '__main__':
    cli = parse_args()

    with cli.infile as input:
        processor = Preprocessor(input.read())

    try:
        processor.process_labels()
    except Exception as exc:
        sys.stderr.write(str(exc))

    with cli.outfile as output:
        output.write(processor.get_result())
