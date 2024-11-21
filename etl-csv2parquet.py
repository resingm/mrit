#!/home/resingm/.pyenv/versions/jupyter/bin/python3

import os
import sys
import uuid

from argparse import ArgumentParser
from glob import glob

import polars as pl

DESC="""
A generic ETL tool to convert a CSV file to a Parquet file.
"""


def generate_partition_paths(base_dir: str, df: pl.DataFrame, *cols) -> dict:
    if len(cols) == 0:
        if os.path.isdir(base_dir) or base_dir.endswith("/"):
            # Supposed to be a folder, or an existing folder
            fpath = os.path.join(base_dir, f"{uuid.uuid4()}.parquet")
        elif not base_dir.endswith(".parquet"):
            fpath = base_dir + ".parquet"
        else:
            fpath = base_dir

        return { fpath: df }
    
    partition_mappings = {}
    
    for row in df.select(cols).unique().collect().rows():
        p_filters = list(zip(cols, row))
        p_mask = [pl.col(c) == v for (c, v) in p_filters]
        p_path = os.path.join(
            base_dir,
            *[f"{c}={v}" for c, v in p_filters],
            f"{uuid.uuid4()}.parquet",
        )
        
        partition_mappings[p_path] = df.filter(*p_mask)
        
    return partition_mappings
    

def main():
    parser = ArgumentParser(
        prog="etl-csv2parquet",
        description=DESC,
    )
    
    parser.add_argument("src", type=str, help="Source path of the CSV file(s)")
    parser.add_argument("dst", type=str, help="Destination path of the Parquet file")
    parser.add_argument("-p", "--partition", help="Columns used to partition output data (separated by `,`)")
    parser.add_argument("-s", "--sort", help="Columns by which to sort (separated by `,`)")
    parser.add_argument("--descending", action="store_true")
    
    args = parser.parse_args()
    
    # Parse arguments
    args.partition = args.partition.split(",") if args.partition else []
    args.sort = args.sort.split(",") if args.sort else []
    
    input_files = glob(args.src)
    
    if len(input_files) <= 0:
        print("No input files match criteria.", file=sys.stderr)
        sys.exit(0)
    
    frames = [pl.scan_csv(fname) for fname in input_files]
    df = pl.concat(frames)
    
    cols = df.collect_schema().names()
    
    if not all(map(lambda c: c in cols, args.partition)):
        print("Invalid column name in partition argument", file=sys.stderr)
        for c in set(args.partition) - set(cols):
            print(f"  Invalid column name: `{c}`", file=sys.stderr)
        sys.exit(1)
    
    if not all(map(lambda c: c in cols, args.sort)):
        print("Invalid column name in sort argument", file=sys.stderr)
        for c in set(args.sort) - set(cols):
            print(f"  Invalid column name: `{c}`", file=sys.stderr)
        sys.exit(1)
    
    if len(args.sort) > 0:
        df = df.sort(*args.sort, descending=args.descending)
        
    partition_mappings = generate_partition_paths(args.dst, df, *args.partition)
    
    for fpath, df_mask in partition_mappings.items():
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        df_mask.sink_parquet(fpath, compression="zstd")
        print(f"Processed partition: {fpath}")
        

if __name__ == "__main__":
    
    main()