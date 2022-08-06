#!/usr/bin/env python3

# ======================================================================
#
#   icanhaz.py
#
# This tool helps to lookup generic BGP features of an IP address. By
# default, it looks up the public IP address via icanhazip.com which
# dubbed this application.
#
# ======================================================================

import sys
import argparse
import requests
import pyasn

USAGE=f"""
{sys.argv[0]} [CMD] [IP]

Lookup BGP features of a given IP. Possible options are listed below.
"""

def main():
    parser = argparse.ArgumentParser(
        description="Lookup some BGP features of a given IP",
        # usage=USAGE,
    )
    parser.add_argument(
        "cmd",
        type=str.lower,
        default="ip",
        choices=["asn", "cidr", "ip"],
        help="Command to specify the feature to return.",
    )
    parser.add_argument(
        "-i",
        "--ip",
        type=str.lower,
        default="127.0.0.1",
        required=False
    )
    parser.add_argument(
        "-v",
        "--ip-version",
        type=int,
        default=4,
        choices=[4, 6],
        help="Define the IP version to lookup ; By default IPv4",
    )
    args = parser.parse_args(sys.argv[1:])

    # Lookup public IP address
    if args.ip in ["127.0.0.1", "::1", "localhost"]:
        # Replace IP if we lookup the localhost
        res = requests.get(f"https://ipv{args.ip_version}.icanhazip.com")
        public_ip = res.text.strip()
        args.ip = public_ip

    # TODO: lookup ASN with pyasn: https://pypi.org/project/pyasn/
    if args.cmd == "asn":
        print("0")
    elif args.cmd == "cidr":
        print("1")
    elif args.cmd == "ip":
        print(args.ip)




if __name__ == "__main__":
    main()