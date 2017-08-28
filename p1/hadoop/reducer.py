#!/usr/bin/env python3

import sys


def log(text):
    with open('log.txt', 'a') as f:
        f.write(text + '\n')


def parse_entry(entry):
    idx = len(entry) - 1 - entry[::-1].find(' ')
    val = float(entry[idx+1:])
    date = entry[:idx]
    return date, val


def main():
    log('\n')
    cdate = ''
    csum = 0.0
    for line in sys.stdin:
        try:
            entry = line.strip()
            log(entry)
            date, val = parse_entry(entry)
            if date != cdate:
                if cdate != '':
                    print('%s %f' % (cdate, csum))
                cdate = date
                csum = val
            else:
                csum += val
        except:
            pass
    if cdate != '':
        print('%s %f' % (cdate, csum))

if __name__ == '__main__':
    main()
