#!/usr/bin/env python3

# ======================================================================
#
#   get_dates_of.py
#
# Tool kit that prints a list of dates to the standard output. The
# prototype can handle weeks. More options will follow.
# 
# TODO:
#   * month
#   * year
#   * between start and end date
#   * more format options
#
# ======================================================================

import argparse
import sys

from datetime import date, timedelta



def err(msg):
    print(msg, file=sys.stderr)


def out(msg):
    print(msg, file=sys.stdout)


def main():
    parser = argparse.ArgumentParser(
        description="Get a list of dates to STDOUT",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="%Y-%m-%d",
    )
    parser.add_argument(
        "-w",
        "--week",
        type=int,
        default=date.today().isocalendar()[1],
        help="Define the week for the days",
    )
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        default=date.today().year,
        help="Define the year of the dates",
    )

    args = parser.parse_args(sys.argv[1:])

    if args.week > 53:
        err("Week cannot be larger than 53")
        sys.exit(1)

    date_start = date.fromisocalendar(args.year, args.week, 1)
    date_end = date.fromisocalendar(args.year, args.week + 1, 1)

    curr = date_start

    while curr < date_end:
        out(curr.strftime(args.format))
        curr += timedelta(days=1)


if __name__ == "__main__":
    main()
