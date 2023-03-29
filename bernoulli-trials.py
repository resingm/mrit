#!/usr/bin/env python3.10

import argparse
import sys
from math import comb, log2, pow

def prob(n, k, p) -> float:
    """Computes the probability of n Bernoulli trials with k successes"""
    # return comb(n, k) * pow(p, k) * pow(1 - p, n - k)
    return pow(p, k) * pow(1 - p, n - k)

def main():
    parser = argparse.ArgumentParser(
        prog="bernulli-trials",
        description="Compute the Bernoulli trials table",
    )
    parser.add_argument("n", type=int, help="Number of trials")
    parser.add_argument("p", type=float, help="Probability of success")
    parser.add_argument("-d", "--digits", type=int, help="Digits to present", default=5)
    args = parser.parse_args(sys.argv[1:])

    n = args.n
    p = args.p
    d = args.digits

    print("n,k,ncr,p(x=k),p(x=k) * ncr", file=sys.stdout)

    for k in range(n + 1):
        ncr = comb(n, k)
        pk = prob(n, k, p)
        pk_ncr = pk * ncr
        chunks = [
            f"{n}",
            f"{k}",
            f"{ncr}",
            f"{pk:0.{d}f}",
            f"{pk_ncr:0.{d}f}",
        ]
        print(",".join(chunks), file=sys.stdout)




if __name__ == "__main__":
    main()

