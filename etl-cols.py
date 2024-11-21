#!/home/resingm/.pyenv/versions/jupyter/bin/python3

import os
import sys
import uuid

from argparse import ArgumentParser
from glob import glob

import polars as pl

DESC="""
A generic ETL tool to select a specific set of columns from a file.

Suppored file formates are `.csv` and `.parquet`.
"""

def select_cols(df: pl.DataFrame, cols: list) -> pl.DataFrame:
    """Selects just the specific set of columns in the given order.

    Args:
        df (pl.DataFrame): The original dataframe
        cols (list): The column selection

    Returns:
        pl.DataFrame: The reduced dataframe
    """
    df = df.select([pl.col(c) for c in cols])
    return df


def main():
    parser = ArgumentParser(
        prog="etl-cols",
        description=DESC,
    )
    
    parser.add_argument("src", type=str, help="Source path of file")
    parser.add_argument("dst", type=str, help="Destination path of the file")
    parser.add_argument("cols", type=str, help="Comma-separated list of column names")
    parser.add_argument("--deduplicate", action="store_true", help="Deduplicate records after selecting specific columns")
    parser.add_argument("--index", action="store_true", help="Add a columns `i` as the row index")
    
    args = parser.parse_args()
    
    if args.src.endswith(".parquet"):
        df = pl.read_parquet(args.src)
    elif args.src.endswith(".csv"):
        df = pl.read_csv(args.src)
    else:
        fext = args.src.split(".")[-1]
        print(f"Cannot read from file with extension `{fext}`; Format not supported.", sys.stderr)
        sys.exit(1)
    
    cols = args.cols.split(",")
    
    df = select_cols(df, cols)
    
    # Deduplicate records if requested
    if args.deduplicate:
        df = df.unique()
        
    # Add the row index column `i` if requested
    if args.index:
        df = df.with_row_index("i")
    
    if args.dst.endswith(".parquet"):
        df.write_parquet(args.dst)
    elif args.dst.endswith(".csv"):
        df.write_csv(args.dst)
    else:
        fext = args.dst.split(".")[-1]
        print(f"Cannot write to file with extension `{fext}`; Format not supported.", sys.stderr)
        sys.exit(1)
        

if __name__ == "__main__":
    main()