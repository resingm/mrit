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
from ipaddress import ip_address
from pprint import pprint as pp

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
        choices=["asn", "cidr", "ip", "ptr"],
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

    # Validate IP input
    try:
        ip_address(args.ip)
    except ValueError:
        print(f"Invalid IP address: {args.ip}")
        sys.exit(1)

    res = requests.get(f"https://api.bgpview.io/ip/{args.ip}")
    
    if not res.ok:
        print(
            f"{res.status_code} - Failed to query {args.ip} from bgpview.io",
            file=sys.stderr,
        )
        sys.exit(1)

    res = res.json()
    if res.get("status", "error") == "error":
        err_msg = res.get("status_message", "<no message>")
        print(
            f"API error: {err_msg}",
            file=sys.stderr,
        )

    # From here on, we can expect a data node
    res = res["data"]

    if args.cmd == "asn":
        answer = "" if len(res["prefixes"]) == 0 else res["prefixes"][0]["asn"]["asn"]
    elif args.cmd == "cidr":
        answer = "" if len(res["prefixes"]) == 0 else res["prefixes"][0]["prefix"]
    elif args.cmd == "ip":
        answer = res["ip"]
    elif args.cmd ==  "ptr":
        answer = "" if res["ptr_record"] is None else res["ptr_record"]
    
    print(answer, file=sys.stdout)




if __name__ == "__main__":
    main()