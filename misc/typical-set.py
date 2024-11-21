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
    parser.add_argument("-k", type=str, help="Range of k in format a..b")
    parser.add_argument("-d", "--digits", type=int, help="Digits to present", default=5)
    args = parser.parse_args(sys.argv[1:])

    n = args.n
    p = args.p
    d = args.digits

    if args.k is None:
        k1, k2 = 0, n+1
    else:
        k1, k2 = args.k.split("..")
        k1, k2 = int(k1), int(k2) + 1
    

    # TODO: Remove ; just for a HW exercise
    hx = sum([
        -1 * p * log2(p),
        -1 * (1 - p) * log2(1 - p),
    ])

    # print("n,k,ncr,p,p(x=k),cum(p(x=k)),1-cum(p(x-k)),H(X),T_NB", file=sys.stdout)
    print(",".join([
        "n",
        "k",
        "nCr",
        "cum(nCr)",
        "p",
        "p(x=k)",
        "p(x<=k)",
        "p(x>k)",
        "H(X)",
        "T_NB",
    ]), file=sys.stdout)

    cum_ncr = 0
    cum_px = 0.0

    for k in range(k1, k2):
        ncr = comb(n, k)
        pk = prob(n, k, p)
        px = pk * ncr

        cum_ncr += ncr
        cum_px += px

        t_nb = abs((1 / n) * log2(1 / pk) - hx)

        chunks = [
            f"{n}",
            f"{k}",
            f"{ncr}",
            f"{cum_ncr}",
            f"{pk:0.{d}f}",
            f"{px:0.{d}f}",
            f"{cum_px:0.{d}f}",
            f"{(1 - cum_px):0.{d}f}",
            f"{hx:0.{d}f}",
            f"{t_nb:0.{d}f}",
        ]

        print(",".join(chunks), file=sys.stdout)

    
    # print(f"Sum of combinations: {sum_ncr}", file=sys.stderr)
    # print(f"Sum of probabilities: {sum_p:0.{d}f}", file=sys.stderr)




if __name__ == "__main__":
    main()

