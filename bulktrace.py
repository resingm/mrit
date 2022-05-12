#!/usr/bin/env python3

# ======================================================================
#
#   bulktrace.py
#
# Tool that bulk-traceroutes a set of IP addresses. The input is read
# from STDIN, the traceroute is processed line by line. The script
# requires [scapy](https://pypi.org/project/scapy/).
#
#
# The output is in CSV, including the source and destination domain/IP
# in each line, in order to map the queries.
# 
# ======================================================================

import subprocess
import sys

BIN = "/usr/bin/traceroute"
ENCODING = "utf-8"

def _parse_hop(*tokens):
    tokens = tokens[1:]

    while len(tokens):
        pass

def _parse_probes(tokens):
    probes = []

    name = ""
    ip = ""
    rtt = 0.0
    annotation = ""

    while len(tokens):
        t1 = tokens.pop(0)

        if t1 == '*':
            # Skip probe wildcards
            while len(tokens) > 0 and tokens[0] == '*':
                tokens.pop(0)
            probes.append(("*", "*", -1.0, ""))
            continue

        t2 = tokens.pop(0).strip(" (),.")

        if t2 == 'ms':
            # Same probe signature with another RTT
            rtt = float(t1)
        else:
            # New probe signature
            t3 = tokens.pop(0)
            # Drop "ms"
            tokens.pop(0)
        
        name, ip, rtt, annotation = t1, t2, float(t3), (tokens.pop(0) if len(tokens) and tokens[0].startswith("!") else "")
        probes.append((name, ip, rtt, annotation))
    
    return probes


def _parse_traceroute(input):
    dest_host = ""
    dest_ip = ""

    # Hops is a list of tuples. Each tuple should have the shape:
    # dest_host, dest_ip, hop_index, probe_index, probe_name, probe_ip, probe_rtt, annotation
    hops = []

    for line in input.split('\n'):
        line = line.strip()
        if not line:
            continue

        if line.lower().startswith("traceroute to "):
            # Title line includes host name and IP
            line = line.replace("traceroute to ", "")
            tokens = line.split()

            if len(tokens) < 2:
                raise ValueError(f"Failed to parse title line: {line}")
                
            dest_host = tokens[0].strip(" (),.")
            dest_ip = tokens[1].strip(" (),.")
        else:
            tokens = line.split()

            if len(tokens) < 4:
                raise ValueError(f"Failed to parse hop line: {line}")

            # Parse hop index
            hop_idx = int(tokens.pop(0))
            for (probe_idx, probe) in enumerate(_parse_probes(tokens)):
                # Generate probe lines for CSV
                rec = (dest_host, dest_ip, hop_idx, probe_idx, *probe)
                hops.append(rec)

    return hops


def _traceroute(target, *args):
    """Calls a traceroute subprocess and parses the results.
    """
    args = [BIN, target] + list(args)
    return subprocess.check_output(args).decode(ENCODING).strip()


def _write_results(results):
    for r in results:
        sys.stdout.write(",".join(map(str, r)))
        sys.stdout.write("\n")
        sys.stdout.flush()


def traceroute(target, *args):
    try:
        tr = _traceroute(target, *args)
        tr = _parse_traceroute(tr)
    except Exception as e:
        sys.stderr(f"Unknown error: {str(e)}")
        return False
    
    _write_results(tr)
    return True


def main():
    # Parse arguments...
    args = []
    header = True
    verbose = False

    for arg in sys.argv[1:]:
        if arg == "--verbose":
            verbose = True
        elif arg == "--no-header":
            header = False
        else:
            args.append(arg)


    if header:
        # Write header to output
        _write_results(["target", "target_ip", "hop", "probe", "host", "host_ip", "rtt", "annotation"])

    # Loop over STDIN and resolve the routes line by line
    try:
        for line in sys.stdin:
            # Prepare the input data ...
            line = line.strip()

            if not line or line[0] == "#":
                # Skip empty lines or in-line comments
                continue

            # Run traceroute
            if verbose:
                sys.stderr.write(f"Traceroute {line} ...")
                sys.stderr.flush()
            res = traceroute(line, *args)
            res = "ok" if res else "failed"

            if verbose:
                sys.stderr.write(f" [{res.upper()}]\n")
                sys.stderr.flush()

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.stderr(f"Unknown error: {str(e)}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()