#!/usr/bin/env python3

# ======================================================================
#
#   bulkdig.py
#
# Small lookup tool that simply reads from STDIN, parses the input line
# by line. Each line that looks like a domain name will be resolved by
# using `dig`. The output will be in CSV format and printed to STDOUT.
#
# ======================================================================

import subprocess
import sys


BIN = "/usr/bin/dig"
ENCODING = "utf-8"


def query_ptr(ip: str, nameserver: str = None):
    ip = ip.lower()

    args = [BIN]
    if nameserver:
        args.append(f"@{nameserver}")

    args.append("+short")
    args.append("-x")
    args.append(ip)

    try:
        return subprocess.check_output(args).decode(ENCODING).strip()
    except subprocess.CalledProcessError:
        return None

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

    try:
        return subprocess.check_output(args).decode(ENCODING).strip()
    except subprocess.CalledProcessError:
        return None


def resolve(
    q,
    nameserver: str = None,
    reverse_lookup: bool = False,
):
    results = []

    if reverse_lookup:
        if q_res := query_ptr(q, nameserver=nameserver):
            for line in q_res.splitlines():
                if len(line) <= 0:
                    continue
                results.append((nameserver, q, "PTR", line))
        else:
            results.append((q, "PTR", "null"))
    else:
        while cname := query(q, "CNAME", nameserver=nameserver):
            results.append(([q, "CNAME", cname]))
            q = cname

        if q_res:= query(q, "A", nameserver=nameserver):
            for line in q_res.splitlines():
                if len(line) <= 0:
                    continue

                results.append((q, "A", line))
        else:
            results.append((q, "A", "null"))

        if q_res := query(q, "AAAA", nameserver=nameserver):
            for line in q_res.splitlines():
                if len(line) <= 0:
                    continue

                results.append((q, "AAAA", line))
        else:
            results.append((q, "AAAA", "null"))

    return results


def main():

    # TODO: Add feature to reverse lookup

    # Parse arguments...
    nameserver = None
    reverse_lookup = False

    for arg in sys.argv:
        arg = arg.strip()
        
        # Check on dig @nameserver argument
        if arg[0] == "@":
            nameserver = arg[1:]
        elif arg == "-x":
            reverse_lookup = True


    # Loop over STDIN and resolve domain names
    try:
        for line in sys.stdin:
            # Prepare the input data ...
            line = line.strip(' \t.\r\n')

            if not line or line[0] == "#":
                # Skip empty lines or in-line comments
                continue

            # Lookup all CNAMES, IPv4 and IPv6
            results = resolve(line, nameserver=nameserver, reverse_lookup=reverse_lookup)

            for r in results:
                sys.stdout.write(",".join(r))
                sys.stdout.write("\n")
                sys.stdout.flush()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
