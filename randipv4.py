#!/usr/bin/env python3

import argparse
import random
import ipaddress
import sys

MAX = 2**32 - 1

def lcg(a, c, seed, n):
    mod = 2**32
    permutations = []
    x = seed
    
    for _ in range(n):
        x = (a * x + c) % mod
        permutations.append(x)
        
    return permutations
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, help="Number of IP addresses to generate; Default 1M", default=10 ** 6)
    parser.add_argument("-s", type=int, help="Seed of the initial address")
    args = parser.parse_args()
    
    # Linear Congruential Generator (LCG)
    # Constants
    a = 1664525
    c = 1013904223
    
    # Define parameters
    n = args.n
    s = args.s if args.s else random.randint(0, MAX)
    
    # Generate random, non-duplicate IP addresses
    for r in lcg(a, c, s, n):
        print(str(ipaddress.IPv4Address(r)), file=sys.stdout)
    

if __name__ == "__main__":
    main()