#!/usr/bin/env python3

# ======================================================================
#
#   filter_ipv4.py
#
# Simply filters on any IPv4 address discovered in the input and prints
# the IPs line by line to STDOUT.
#
# ======================================================================

from functools import reduce
import re
import sys

ipv4_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

def main():
    matches =[re.findall(ipv4_pattern, line) for line in sys.stdin]

    for m in reduce(lambda a, b: a + b, matches):
        print(m)


if __name__ == "__main__":
    main()
