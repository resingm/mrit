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

import asyncio
import subprocess
import sys
import time

BIN = "/usr/bin/traceroute"
ENCODING = "utf-8"
# Limit on the number of traceroute calls
SUBPROCESS_SEMAPHORE_LIMIT = 64


def stderr(msg):
    sys.stderr.write(msg)
    sys.stderr.write("\n")
    sys.stderr.flush()


def stdout(results):
    for r in results:
        sys.stdout.write(",".join(map(str, r)))
        sys.stdout.write("\n")
        sys.stdout.flush()


def _parse_probes(tokens):
    """Parses a set of probes and returns them as a list of tuples."""
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
            # Thus, fill the tokens to be parsed properly at the end of
            # the while loop
            t3 = t1
            t2 = ip
            t1 = name
        else:
            # New probe signature
            t3 = tokens.pop(0)
            # Drop "ms"
            tokens.pop(0)
        
        name, ip, rtt, annotation = t1, t2, float(t3), (tokens.pop(0) if len(tokens) and tokens[0].startswith("!") else "")
        probes.append((name, ip, rtt, annotation))
    
    return probes


def _parse_traceroute(input):
    """Reads the input of a traceroute and parses it to allow the
    generation of a CSV file.
    """
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


async def _traceroute(target, *args):
    """Calls a traceroute subprocess and parses the results.
    """
    args = [BIN, target] + list(args)
    # return subprocess.check_output(args, stderr=subprocess.PIPE).decode(ENCODING).strip()
    p = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    out, err = await p.communicate()

    if p.returncode == 0:
        return out.decode(ENCODING).strip()
    else:
        raise subprocess.CalledProcessError(
            p.returncode,
            " ".join(args),
            out,
            err,
        )



def drop_complete(tasks):
    """Should be called if at least one task is done (e.g. the semaphore
    is NOT locked. Then, the complete tasks are dropped and new can be
    scheduled.
    """
    tmp = []
    for task in tasks:
        if task.done():
            handle_task(task)
        else:
            tmp.append(task)
        
    return tmp


def handle_task(task: asyncio.Task):
    """Handles the result of a task and prints some information to the
    STDERR. The STDOUT is not affected.
    """
    name = task.get_name()
    
    try:
        if e := task.exception():
            stderr(f"[EE] {name} failed: {str(e)}")
        else:
            stderr(f"[OK] {name} done")
    except asyncio.CancelledError:
        stderr(f"[!!] {name} cancelled")
    except asyncio.InvalidStateError:
        stderr(f"[EE] {name} is still running. Task cannot be handled. This is a programming error.")



async def traceroute(target, semaphore: asyncio.Semaphore, *args):
    """Async call to manage the traceroute. Can be called as a task to
    give it a name to handle potential failure.
    """
    # Await to acquire the semaphore
    await semaphore.acquire()

    try:
        tr = await _traceroute(target, *args)
        tr = _parse_traceroute(tr)
        stdout(tr)
    except Exception as e:
        raise e
    finally:
        semaphore.release()


async def main():
    # Parse arguments...
    args = []
    header = True
    verbose = False

    # Keep track of the return code
    rc = 0

    # Define a semaphore to limit number of async subprocesses
    semaphore = asyncio.Semaphore(value=SUBPROCESS_SEMAPHORE_LIMIT)
    # Define a task list to join on
    tasks = []


    for arg in sys.argv[1:]:
        if arg == "--verbose":
            verbose = True
        elif arg == "--no-header":
            header = False
        else:
            args.append(arg)


    if header:
        # Write header to output
        stdout([("target", "target_ip", "hop", "probe", "host", "host_ip", "rtt", "annotation")])

    demo = ["176.9.40.199"]

    # Loop over STDIN and resolve the routes line by line
    try:
        #for line in sys.stdin:
        for line in demo:
            while semaphore.locked():
                await asyncio.sleep(1)
            # Remove complete tasks to let GC cleanup memory if all
            # tasks are currently running
            tasks = drop_complete(tasks)

            # Prepare the input data ...
            line = line.strip()

            if not line or line[0] == "#":
                # Skip empty lines or in-line comments
                continue

            # Run traceroute
            if verbose:
                stderr(f"[  ] Traceroute {line}")

            task = asyncio.create_task(
                traceroute(line, semaphore, *args), name=line
            )
            tasks.append(task)
            # Pass on the round robin...
            await asyncio.sleep(0.1)


    except KeyboardInterrupt:
        rc = 255
    except Exception as e:
        stderr(f"[EE] Unknown error: {str(e)}")
        rc = 1

    if rc > 0:
        # Cancel all tasks on a failure or interrupt.
        for task in tasks:
            task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

    while len(tasks):
        task = tasks.pop(0)
        handle_task(task)

    sys.exit(rc)


if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    stderr(f"Execution time: {elapsed:0.2f} seconds")