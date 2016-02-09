# -*- coding: utf-8 -*-
"""Script for cleaning parallel corpora based on dictionary and stop words

Script count two numbers:
    m - total number of words in sentence (excluding stop words)
    n - total number of words in sentence from dictionary
Filtering can be done using absolute and relative difference:
    abs_diff = n
    rel_diff = n/m
Sentence will be preserved if absolute or relative difference is more for it
then provided in script options

Example command:
    $ python sentence_cleaner.py --abs_diff 3 --dictionary dictionary.txt --stop_words stop.txt text1 text2

Cleaned sentences will be saved as "cleaned__[file_name]"
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import re
import os
import logging
from argparse import ArgumentParser, RawTextHelpFormatter
from codecs import open as copen
from itertools import izip

punct_re = re.compile(u'[!"#$%&\'()*+,-./:;<=>?@[\\\\\\]\\^_`{|}~]')
log = logging.getLogger()

def main(args):
    dict_w = []
    stop_w = []
    if args.dictionary:
        dict_w = load_dictionary(args.dictionary)
    if args.stop_words:
        stop_w = load_dictionary(args.stop_words)
    file1 = copen(gen_name(args.paths[0]), 'w', encoding='utf-8')
    file2 = copen(gen_name(args.paths[1]), 'w', encoding='utf-8')
    for i, pair in enumerate(line_iter(*args.paths)):
        if is_ok(dict_w, stop_w, pair, abs_t=args.abs_diff, rel_t=args.rel_diff):
            file1.write(pair[0])
            file2.write(pair[1])
        if i % 1000 == 0:
            log.info('Lines processed %i', i+1)
    file1.close()
    file2.close()

def gen_name(path):
    """TODO: Docstring for gen_name.

    :path: TODO
    :returns: TODO

    """
    d = os.path.dirname(path)
    n = os.path.basename(path)
    n = 'cleaned___' + n
    return os.path.join(d, n)

def line_iter(path1, path2):
    file1 = copen(path1, encoding='utf-8')
    file2 = copen(path2, encoding='utf-8')
    for p_line in izip(file1, file2):
        yield p_line
    file1.close()
    file2.close()

def load_dictionary(path):
    """TODO: Docstring for load_dictionary.

    :path: TODO
    :returns: TODO

    """
    with copen(path) as f:
        words = (w.strip().lower() for w in f)
        words = set(words)
        return words

def tokenize(sent):
    sent = sent.lower()
    sent = punct_re.sub(u' ', sent).strip()
    sent = sent.split()
    return sent

def clean_words(words, tokens):
    return [t for t in tokens if t not in words]

def dif(words, tokens):
    m = len(tokens)
    tokens = [t for t in tokens if t in words]
    n = len(tokens)
    return m, n

def is_ok(dict_w, stop_w, pair, abs_t=None, rel_t=None):
    tokens = tokenize(pair[0])
    tokens = clean_words(stop_w, tokens)
    m, n = dif(dict_w, tokens)
    if abs_t is not None:
        if n < abs_t:
            return False
    if rel_t is not None:
        try:
            r = n/m
            if r < rel_t:
                return False
        except ZeroDivisionError:
            return False
    return True

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument('paths', nargs=2, help='Path to 2 files with parallel corpora for filtering')
    parser.add_argument('--dictionary', help='Path to dictionary')
    parser.add_argument('--stop_words', help='Path to stop words')
    parser.add_argument('--abs_diff', type=int, default=None, help='Minimal absolute difference for saving sentence pair')
    parser.add_argument('--rel_diff', type=float, default=None, help='Minimal relative difference for saving sentence pair')
    main(parser.parse_args())
