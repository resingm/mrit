#!/bin/bash

if [[ $# -ne 1 ]] ; then
    echo "Usage: $0 <column_index>"
fi

column_index=$1

# awk can extract the column index.
awk -F ',' '{print $'"$column_index"'}'