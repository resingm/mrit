#!/usr/bin/env python3

import argparse
import ipaddress
import sys

DESCR="""
Reads a list of IP addresses from STDIN and groups them together to CIDR
blocks. If a critical mass of IP addresses is reached, it returns the
CIDR block, instead of the individual IP address.

Note: At this moment, the tool only supports /24 and /48 CIDR blocks for
IPv4 and IPv6 respectively. Smart grouping algorithms are desireable,
but yet to be implemented.
"""

buf = {}

ipv4_prefix = "/24"
ipv6_prefix = "/64"

def main():
    """Main functon to handle the parsing and grouping."""
    parser = argparse.ArgumentParser(
        description=DESCR,
    )

    parser.add_argument(
        "-n",
        "--group-size",
        type=int,
        default=16,
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
    )

    args = parser.parse_args()

    lines = None
    if args.file:
        with open(args.file, "r") as f:
            lines = f.readlines()

    for l in (lines if lines is not None else sys.stdin):
        l = l.strip()

        if len(l) == 0 or l[0] == "#":
            continue

        # TODO: Consider CIDR notation too, and unroll subnets smaller /32 or /128

        ip = ipaddress.ip_address(l)
        subnet = "/24" if ip.version == 4 else "/48"
        cidr = ipaddress.ip_network(l + subnet, strict=False)
        buf[cidr] = buf.get(cidr, []) + [ip]

    for cidr, ip_group in buf.items():
        if len(ip_group) >= args.group_size:
            print(f"{str(cidr)}", file=sys.stdout)
        else:
            for ip in ip_group:
                subnet = "/32" if ip.version == 4 else "/128"
                print(f"{str(ip)}{subnet}", file=sys.stdout)


if __name__ == "__main__":
    main()
