#!/usr/bin/env python3

# ======================================================================
# 
#   ipinfo.py
#
# Small lookup tool that simply reads from STDIN, parses the input line
# by line and lookups the IP information from ipinfo.io. Non-valid IP
# inputs are simply discarded.
# The results are written to STDOUT, which makes the tool suitable to be
# used within shellscripts and pipes.
#
# Requires a configuration in $HOME/.config/mrit.ini as follows
#
# ======================================================================

import configparser
import ipaddress
import json
import os
import sys
import requests

from pathlib import Path

BASE_URI = "ipinfo.io"


def fetch(ip, token):
    req = f"https://{BASE_URI}/{ip}?token={token}"
    res = requests.get(req)
    
    if not res.ok:
        return None
    
    return res.json()


def err(msg, do_flush=True):
    sys.stderr.write(msg)
    sys.stderr.write('\n')
    
    if do_flush:
        sys.stderr.flush()

def write(data, do_flush=True):
    sys.stdout.write(data)
    sys.stdout.write('\n')

    if do_flush:
        sys.stdout.flush()


def main():
    # Load config
    cfg_file = os.path.join(
        Path.home(),
        '.config/mrit.ini',
    )

    if not os.path.isfile(cfg_file):
        err(f"Cannot find file {cfg_file}.")
        err("File will be generated but requires you to add the API token to the configuration file.")

        with open(cfg_file, 'w') as f:
            f.writelines([
                "[ipinfo]\n",
                "token = \n",
            ])

        err(f"Template written to {cfg_file}")
        err("Exiting ...")
        sys.exit(1)

    # Load config
    cfg = configparser.ConfigParser()
    cfg.read(cfg_file)
    ipinfo_token = cfg.get('ipinfo', 'token')

    if not ipinfo_token:
        err(f"Token not configured in {CFG}")
        sys.exit(1)

    try:
        # Reads from STDIN and writes to STDOUT
        for _in in sys.stdin:
            # Prepare the input data ...
            _in = _in.strip()

            try: 
                ipaddress.ip_address(_in)
            except Exception as e:
                # Ignore IPs that cannot be parsed
                continue

            # ... fetch the IP info ...
            ipinfo = fetch(_in, ipinfo_token)

            # ... and write to STDOUT
            if ipinfo:
                ipinfo = json.dumps(ipinfo)
                write(ipinfo)
    except KeyboardInterrupt:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()