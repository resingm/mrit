#!/bin/bash

host="whois.cymru.com"

usage() {
    echo "Usage: $0 [-46] [input_file]"
    echo ""
    echo "This scripts performs a lookup of IP addresses. It will send a whois request"
    echo "to Team Cymru's whois service. Besides the regular lookup, one can also lookup"
    echo "the IP's peering networks, e.g. one hop away from the originating ASN. This is"
    echo "handy to understand the upstream providers of a given IP address."
    echo ""
    echo "Options:"
    echo "  -4      Enforces the usage of IPv4 for data transmission"
    echo "  -p      Looks up the first hop of an IP address."
    echo ""
    echo "Examples:"
    echo "  $0 -4 input_file.txt    # Performs a whois lookup by using the IPv4 service"
    echo "  cat input_file | $0     # Performs a lookup by reading from STDIN"
    echo ""
    exit 1
}

# Parser command line arguments
while getopts "4p" opt; do
    case $opt in
        4)
            host="v4.whois.cymru.com"
            ;;
        p)
            host="v4-peer.whois.cymru.com"
            ;;
        h)
            usage
            ;;
        *)
            usage
            ;;
    esac
done

# Shift parsed options so $1 becomes the input file if provided
shift $((OPTIND - 1))


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

