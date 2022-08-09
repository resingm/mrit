#!/usr/bin/env python3

# ----------------------------------------------------------------------
#
#   wait4ip.py
#
# Tool is supposed to serve a single purpose: After starting an OpenVPN
# connection with a shell script, the script should block until the
# prefix has changed.
#
# Requires a single argument, which was a IP lookup before the OpenVPN
# startup. This ensures that the script does not block indefinitely
# accidentally.
#
# The script blocks for 2 seconds between each lookup. The public IP is
# determined based on the service https://icanhazip.com
#
# Sample usage:
#
# ```
#   wait_for_connection() {
#       ip=$(curl -s https://ipv4.icanhazip.com)
#       result=$(./wait4ip.py $ip)
#       return $result
#   }
#   
#   if wait_for_connection ; then
#       echo "success"
#   else
#       echo "failure"
#   fi
# ```
#
# Caveat: So far, it just supports IPv4 since this was most pressing.
#
# ----------------------------------------------------------------------

from ipaddress import ip_network
from time import sleep

import sys

import requests

def query_ip(use_v6: bool = False):
    uri = "https://ipv4.icanhazip.com"
    if use_v6:
        uri = "https://ipv6.icanhazip.com"

    res = requests.get(uri)

    if not res.ok:
        raise Exception("Failed")

    return res.text.strip()


def main():
    # Make sure we get an IP address as an argument
    if len(sys.argv) < 2:
        print(1, file=sys.stdout)
        sys.exit(1)

    old_ip = ip_network(f"{sys.argv[1]}/24", strict=False)

    attempts_left = 5

    while attempts_left > 0:
        # Decrease counter
        attempts_left -= 1
        sleep(2)

        # Fetch public IP
        try:
            curr_ip = query_ip()
        except:
            continue

        curr_ip = ip_network(f"{curr_ip}/24", strict=False)

        if old_ip != curr_ip:
            # Success, we get a new IP
            print(0, file=sys.stdout)
            sys.exit(0)
    
    print(1, file=sys.stdout)
    sys.exit(1)




    

if __name__ == "__main__":
    main()