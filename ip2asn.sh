#!/bin/bash

host="whois.cymru.com"

# Trap the temporary directory to delete on EXIT
TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT


# Input file
bulk="$TMP/bulk.txt"

echo "begin" >> $bulk
echo "verbose" >> $bulk
# TODO: Add a filter on IPv4 and IPv6.
cat "${1:-/dev/stdin}" | sort | uniq >> $bulk
echo "end" >> $bulk

tmp_lookup=$(mktemp)

netcat $host 43 < $bulk >> ${tmp_lookup}

# Print CSV header
echo "asn,ip,prefix,cc,rir,allocated,asname"

# Convert IP-to-ASN output to CSV
cat ${tmp_lookup} | grep "^[0-9]" | sed -E 's/\| ([^|]+)$/| "\1"/' | sed 's/ *| */,/g'

