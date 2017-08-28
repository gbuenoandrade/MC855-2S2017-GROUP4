#!/usr/bin/env python3

import sys
import os
from analyzer import *


def log(text):
    with open('log.txt', 'a') as f:
        f.write(text + '\n')


def read_tweet(entry):
    idx1 = entry.find(' ')
    idx2 = entry.find(' ', idx1+1)
    date = entry[0:idx1]
    score = float(entry[idx1+1:idx2])
    text = entry[idx2+1:]
    return date, score, text


def main():
    anlysr = Analyzer(os.getcwd())
    for line in sys.stdin:
        try:
            entry = line.strip()
            date, score, text = read_tweet(entry)
            val = anlysr.classify(text) * score
            log('%s %f %s' % (date, val, text))
            print('%s %f' % (date, val))
        except:
            pass

if __name__ == '__main__':
    main()
