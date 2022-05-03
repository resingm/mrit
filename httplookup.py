#!/usr/bin/env python3

# ======================================================================
#
#   httplookup.py
#
# Lookup web server responses in bulk and log the results. Pipe a list
# of domains you want to check to this tool, receive a list of HTTP(s)
# responses to STDOUT.
#
# The tool tests both on HTTP and HTTPS.
# 
# ======================================================================

# import json
import sys
import uuid

from datetime import datetime

import requests
import ujson

class Response:
    # uniquely generated ID
    id: int
    # lookup sequence of request based on ID
    seq: int
    # Requested timestamp
    ts: int
    # Requested URL
    url_req: str
    # URL of the response
    url_res: str
    # Elapsed time in microseconds
    elapsed: int
    # Status code of the response
    status_code: int
    # Dictionary of the header fields
    headers: dict
    # Cookies
    cookies: dict
    # Links
    links: dict
    # Raw body
    body: str

    def __init__(self):
        pass

    def to_json(self):
        return ujson.dumps(
            self,
            # indent=0,
            # separators=(',', ':'),
            default=lambda o: o.__dict__,
            # sort_keys=False,
        )



def query(url: str):
    """Query a given URL, merge the lookup history, by following redirects and
    return the results in chronological order.
    """

    results = []

    # Unique identifier
    id = str(uuid.uuid4())
    # POSIX timestamp
    ts = int(datetime.now().timestamp())
    res = requests.get(url)

    responses = [x for x in res.history]
    responses.append(res)


    for seq, x in enumerate(responses):
        try:
            content = x.text
        except Exception as e:
            text = str(e)

        r = Response()
        r.id = id
        r.seq = seq
        r.ts = ts
        r.url_req = url
        r.url_res = x.url
        r.elapsed = x.elapsed.microseconds
        r.status_code = x.status_code
        r.headers = x.headers
        r.cookies = x.cookies._cookies
        r.links = x.links
        r.body = x.text

        results.append(r)

    return results


def http(url):
    """Lookup as HTTP"""
    return query("http://" + url)


def https(url):
    """Lookup as HTTPS"""
    return query("https://" + url)


def main():
    # Parse arguments...
    # for arg in sys.argv:
    #    arg = arg.strip()
        
    # Loop over STDIN and query HTTP requests
    try:
        for line in sys.stdin:
            # Prepare the input data ...
            line = line.strip()

            if not line or line[0] == "#":
                # Skip empty lines or in-line comments
                continue

            # Lookup all CNAMES, IPv4 and IPv6
            # results = resolve_domain_name(line, nameserver=nameserver)
            results = []

            results += http(line)
            results += https(line)

            for r in results:
                sys.stdout.write(r.to_json())
                sys.stdout.write("\n")
            
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()