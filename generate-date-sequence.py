#!/usr/bin/python3

import argparse
import sys
from datetime import date, timedelta

DESC="""
Generate sequences of dates and prints the dates in ISO 8601 format to STDOUT.
Requires a first and last date.

The last date is exclusive. This is mostly due to the common case, where you
define the date range per month from e.g. 2024-01-01 to 2024-02-01, meaning that
the last date would be exclusive.
"""

def main():
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("first", help="First date", type=date.fromisoformat)
    parser.add_argument("last", help="Last date (exclusive)", type=date.fromisoformat)
    parser.add_argument("--header", help="Define if a header should be printed", type=str, default=None)
    parser.add_argument("-t", "--ticks", help="Define the tick every `n` days; Default is `1`", default=1, type=int)
    args = parser.parse_args()

    curr = args.first
    stop = args.last
    delta = args.ticks

    if args.header:
        print("ts", file=sys.stdout)

    while curr < stop:
        print(curr.isoformat(), file=sys.stdout)
        curr += timedelta(days=delta)


if __name__ == "__main__":
    main()
