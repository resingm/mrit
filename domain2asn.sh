#!/bin/bash

host="whois.cymru.com"

# Trap the temporary directory to delete on EXIT
TMP_A=$(mktemp)
TMP_AAAA=$(mktemp)

trap "rm -rf $TMP_A" EXIT
trap "rm -rf $TMP_AAAA" EXIT

# echo $1
fqdns="${1:-$(cat /dev/stdin)}"

for fqdn in $fqdns ; do
  # Query A & AAAA records
  dig +short A "${fqdn}" >> "$TMP_A"
  dig +short AAAA "${fqdn}" >> "$TMP_AAAA"
done

if [[ -s $TMP_A ]] ; then
  echo "-----------------------------------------------------------------------------------------" 
  whois -h "${host}" "-v $(cat ${TMP_A})" | grep -v "Warning: RIPE flags used"
  echo ""
else
  # echo "" >&2
  echo "No A record found" >&2
fi

if [[ -s "${TMP_AAAA}" ]] ; then
  echo "-----------------------------------------------------------------------------------------------------------------"
  whois -h "${host}" "-v $(cat ${TMP_AAAA})" | grep -v "Warning: RIPE flags used"
  echo ""
else
  # echo "" >&2
  echo "No AAAA record found" >&2
fi

