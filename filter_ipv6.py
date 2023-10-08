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

# WARNING: This is highly inacurate and only filters IPv6 out of a list
#          of IPv4 and IPv6
ipv6_pattern = f"[0-9a-fA-F:]+"

def main():
    matches =[re.findall(ipv6_pattern, line) for line in sys.stdin]

    for m in reduce(lambda a, b: a + b, matches):
        print(m)


if __name__ == "__main__":
    main()
