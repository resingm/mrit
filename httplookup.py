#!/usr/bin/env python3

# ======================================================================
#
#   httplookup.py
#
# Lookup web server responses in bulk and log the results. Pipe a list
# of domains you want to check to this tool, receive a list of HTTP(s)
# responses to STDOUT.
#
# The tool tests both on HTTP and HTTPS.
# 
# ======================================================================


import asyncio
import json
import sys
import time
import uuid

from datetime import datetime

import aiohttp
from aiolimiter import AsyncLimiter


# 8 requests / second
limiter = AsyncLimiter(1, 0.125)


def err(msg, do_flush=True):
    sys.stderr.write(msg)
    sys.stderr.write('\n')

    if do_flush:
        sys.stderr.flush()


class Response:
    # uniquely generated ID
    id: int
    # lookup sequence of request based on ID
    seq: int
    # Requested timestamp
    ts: int
    # Requested URL
    url_req: str
    # URL of the response
    url_res: str
    # Status code of the response
    status_code: int
    # Dictionary of the header fields
    headers: dict
    # Cookies
    cookies: dict
    # Raw body
    body: str
    # body length:
    length: int
    # Python error message
    err_msg: str

    def __init__(self):
        pass

    def to_json(self):
        return json.dumps(
            self,
            # indent=0,
            # separators=(',', ':'),
            default=lambda o: dict([(k, str(v)) for k, v in o.__dict__.items()]),
            # sort_keys=False,
        )



async def query(url: str, semaphore: asyncio.Semaphore):
    """Query a given URL, merge the lookup history, by following redirects and
    return the results in chronological order.
    """

    results = []
    responses = []

    # Unique identifier
    r_id = str(uuid.uuid4())
    # POSIX timestamp
    r_ts = int(datetime.now().timestamp())
    r_url_req = url

    async with aiohttp.ClientSession() as session:
        # Wait for it's semaphore
        await semaphore.acquire()

        try:
            err(f"Fetching {url} ...")
            async with session.get(url, timeout=7) as res:
                responses += res.history
                responses.append(res)

                for seq, x in enumerate(responses):
                    try:
                        err_msg = ""
                        content = await x.text()
                    except Exception as e:
                        content = ""
                        err_msg = str(e)

                    r = Response()
                    r.id = r_id
                    r.seq = seq
                    r.ts = r_ts
                    r.url_req = r_url_req
                    r.url_res = str(x.url)
                    r.status_code = x.status
                    r.headers = dict(x.raw_headers)
                    r.cookies = dict(x.cookies)
                    r.body = content
                    r.length = x.content_length
                    r.err_msg = err_msg

                    results.append(r)

        except Exception as e:
            r = Response()
            r.id = r_id
            r.seq = 0
            r.ts = r_ts
            r.url_req = r_url_req
            r.url_res = ""
            r.status_code = -1
            r.headers = None
            r.cookies = None
            r.body = ""
            r.length = -1
            r.err_msg = str(e)
            results.append(r)
        finally:
            semaphore.release()

    return results


async def main():

    # Prepare list of URLs to fetch
    urls = []

    for line in sys.stdin:
        line = line.strip()

        if not line or line[0] == '#':
            # Skip empty lines or in-line comments
            continue

        if line.startswith('http://'):
            urls.append(line)
        elif line.startswith('https://'):
            urls.append(line)
        else:
            urls.append('http://' + line)
            urls.append('https://' + line)


    semaphore = asyncio.Semaphore(value=16)
    tasks = []
    #await query(urls, semaphore)

    # async with aiohttp.ClientSession() as session:
    #    await semaphore.acquire()

    for url in urls:
        tasks.append(query(url, semaphore))
    
    # await asyncio.wait(tasks)
    results = await asyncio.gather(*tasks)

    for responses in results:
        for response in responses:
            sys.stdout.write(response.to_json())
            sys.stdout.write("\n")

        sys.stdout.flush()


if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    err(f"Execution time: {elapsed:0.2f} seconds")
