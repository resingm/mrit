#!/usr/bin/env python3

import argparse
import json
import os
import sys
from urllib.parse import unquote_plus


def disassemble_endpoint(base_url):
    proto, r = base_url.split("://", maxsplit=1)
    region, _ = r.split(".", maxsplit=1)
    fqdn, _ = r.split("/", maxsplit=1)

    return {
        "protocol": proto,
        "region": region,
        "fqdn": fqdn,
        "uri": base_url,
    }



def main():
    parser = argparse.ArgumentParser(
            "safelink-disassembler",
            description="Disassemble safelinks and print them in a more readable format",
    )
    parser.add_argument("safelink")

    args = parser.parse_args(sys.argv[1:])

    endpoint, data = args.safelink.split("?")
    params = data.split("&")
    params = [tuple(e.split("=")) for e in params if len(e) > 0]
    params = [(e[0], unquote_plus(e[1])) for e in params]

    # Build struct around the endpoint
    struct = { "_meta": disassemble_endpoint(endpoint) }
    struct.update(dict(params))

    # Further disassembling the data
    disassembled = {}

    if "data" in struct:
        disassembled["data"] = struct["data"].split("|")

    if disassembled:
        struct["_disassembled"]  = disassembled



    print(json.dumps(struct))

if __name__ == "__main__":
    main()
