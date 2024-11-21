#!/home/resingm/.pyenv/versions/jupyter/bin/python3

import argparse
import glob
import gzip
import json
import os

import polars as pl

KEYS_IGNORE = ["_shodan"]
KEYS_CONTEXT = ["http", "ssl", "location", "opts"]
KEYS_PRIMITIVE = ["timestamp", "ip_str", "ip", "asn", "isp", "org", "hash", "product", "os", "tags", "hostnames", "domains", "transport", "port", "data"]


# -------------------------------------------------------------
# File loading functions
# -------------------------------------------------------------
def load_input_data(dpath: str) -> list:
    """Loads all JSON files from a folder into Python dictionaries."""
    data = []

    for fpath in glob.glob(dpath):
        if fpath.endswith(".gz"):
            with gzip.open(dpath) as f:
                data += [json.loads(l) for l in f.readlines()]
        else:
            with open(fpath, "r") as f:
                data += [json.loads(l) for l in f.readlines()]
                
    return data


# -------------------------------------------------------------
# Context loading functions
# -------------------------------------------------------------
def load_context_http(ctx) -> dict:
    """Loads predefined fields from the HTTP context."""
    data = {k: v for k, v in ctx.items() if k in ["status", "title", "server", "html"] }
    return data

def load_context_location(ctx) -> dict:
    """Loads predefined fields from the location context."""
    data = {k: v for k, v in ctx.items() if k in ["country_code", "latitude", "longitude"] }
    return data

def load_context_opts(ctx) -> dict:
    """Loads context for the opts field."""
    data = {k: v for k, v in ctx.items() if k in ["vulns"]}
    return data

def load_context_ssl(ctx) -> dict:
    """Loads predefined fields from the SSL context."""
    data = {k: v for k, v in ctx.items() if k in ["cipher", "ja3s", "jarm", "trust", "versions"] }
    
    # Fill certificate information
    data["cert"] = {}
    cert = ctx.get("cert", {})
    for k in ["expired", "expires", "issued", "issuer", "pubkey", "sig_alg", "subject", "version"]:
        data["cert"][k] = cert.get(k, None)

    return data

def load_context(label, ctx) -> dict:
    """Just a router function to be called with the context label and the data as a dictionary."""
    if label == "http":
        return load_context_http(ctx)
    elif label == "location":
        return load_context_location(ctx)
    elif label == "opts":
        return load_context_opts(ctx)
    elif label == "ssl":
        return load_context_ssl(ctx)
    else:
        return {}


def sanitize_records(records: list) -> list:
    """Sanitizes a list of input records to ensure uniformity"""
    sanitized_records = []    

    for i, r in enumerate(records):
        rec = {"i": i}
        
        # Load primitive keys
        rec.update({ k: v for k, v in r.items() if k in KEYS_PRIMITIVE })

        # Load context keys
        rec.update({ k: load_context(k, r.get(k, {})) for k in KEYS_CONTEXT })

        # Append to records
        sanitized_records.append(rec)

    return sanitized_records


def main():
    """The main function - Turning the cogs..."""

    # TODO: Add description for the tool, etc.
    parser = argparse.ArgumentParser()
    parser.add_argument("srcpath", help="Define a source path where to read the data from", type=str)
    parser.add_argument("dstfile", help="Destination to store the parquet file")

    args = parser.parse_args()

    input_data = load_input_data(args.srcpath)
    records = sanitize_records(input_data)
    df = pl.DataFrame(records, infer_schema_length=None)
    df.write_parquet(args.dstfile, compression="zstd")


if __name__ == "__main__":
    main()
