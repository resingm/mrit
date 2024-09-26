#!/usr/bin/env python3

import argparse
import json
import os
import sys
from urllib.parse import unquote_plus


link="https://eur02.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.integrand.nl%2F&data=05%7C01%7Cs.s.spuls%40utwente.nl%7C6aa76a69803f4f56299b08dbbf69d46b%7C723246a1c3f543c5acdc43adb404ac4d%7C0%7C0%7C638314233487847100%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=f8OUXgkqULnWjhGbCmk%2FVtHiis9q%2FsbCxKeORTEaWdo%3D&reserved=0"


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
    params = [(e[0].replace("amp;", ""), unquote_plus(e[1])) for e in params]

    # Build struct around the endpoint
    struct = { "_meta": { "endpoint": endpoint } }
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
