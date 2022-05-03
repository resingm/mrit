#!/usr/bin/env python3

# ======================================================================
#
#   massdig.py
#
# Small lookup tool that simply reads from STDIN, parses the input line
# by line. Each line that looks like a domain name will be resolved by
# using `dig`. The output will be in CSV format and printed to STDOUT.
# 
# ======================================================================

import json
import os
import subprocess
import sys


BIN = "/usr/bin/dig"
ENCODING = "utf-8"


def query(domain_name: str, qtype: str, nameserver: str = None):
    domain_name = domain_name.lower()
    qtype = qtype.upper()

    # TODO: Add filter to query type
    # if qtype not in ['A', 'AAAA', 'CNAME', ...]
    args = [BIN]

    if nameserver:
        args.append(f"@{nameserver}")

    args.append(domain_name)
    args.append(qtype)
    args.append("+short")

    return subprocess.check_output(args).decode(ENCODING).strip()


def resolve_domain_name(domain_name, nameserver: str = None):
    results = []

    while cname := query(domain_name, "CNAME", nameserver=nameserver):
        results.append(([domain_name, "CNAME", cname]))
        domain_name = cname

    if ipv4 := query(domain_name, "A", nameserver=nameserver):
        results.append((domain_name, "A", ipv4))
    else:
        results.append((domain_name, "A", "null"))

    if ipv6 := query(domain_name, "AAAA", nameserver=nameserver):
        results.append((domain_name, "AAAA", ipv6))
    else:
        results.append((domain_name, "AAAA", "null"))

    return results


def main():

    # TODO: Add arg parse for nameserver
    # TODO: Add feature to reverse lookup

    try:
        for line in sys.stdin:
            # Prepare the input data ...
            line = line.strip()

            if not line:
                # Skip empty lines
                continue

            if line[0] == '#':
                # Skip in-line comments
                continue

            # Lookup all CNAMES, IPv4 and IPv6
            results = resolve_domain_name(line)

            for r in results:
                sys.stdout.write(",".join(r))
                sys.stdout.write("\n")
                sys.stdout.flush()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()