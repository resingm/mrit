#!/bin/bash

# ----------------------------------------------------------------------
#
# csv-col.sh
#
# Parses a CSV file and returns the column defined by the `COL` param.
#
# by Max Resing <contact@maxresing.de>
#
# ----------------------------------------------------------------------

SEMAPHORE=unique-id
VERSION=0.1.0

function usage() {
    cat << EOF
Usage: $0 [OPTION]
Parses a CSV file and returns the column defined by the -c parameter.
This tool can only parse CSVs without quoted fields. It simply splits
rows on the delimiter. By default, the first row (header) is skipped and
the first column is returned. Also 'null' values are skipped.

  -c    column index, starting with 0
  -d    delimiter to split fields, default: ,
  -f    read from file, default from STDIN
  -h    display this help and exit
  -H    not skip the header row
  -n    not skip 'null' values in output
  -v    output version information and exit

Examples:
    $0 -c2 -d;      Read STDIN, split on ';' and get 2nd col
    $0              Read STD, split on ',' and get 1st col

  by Max Resing <contact@maxresing.de>

EOF
}


# --- Option processing --------------------------------------------
col=0
delimiter=","
input_file="/dev/stdin"
skip_lines=2
skip_null=1


# Parsing arguments
while [ ! -z "$1" ] ; do
  case "$1" in
    --col|-c)
      # Define the column index
      shift
      col=$1
      ;;
    --delimiter|-d)
      # Define a custom delimiter
      shift
      delimiter=$1
      ;;
    --file|-f)
      # Read from file instead of standard input
      shift
      input_file=$1
      ;;
    --header|-H)
      # Not skip the header
      skip_lines=1
      ;;
    --include-null|-n)
      # Include 'null' in output
      skip_null=0
      ;;
    --help|-h)
      # Print help and exit
      usage
      exit 0
      ;;
    --version|-v)
      # Print version and exit
      echo "Version $VERSION"
      exit 0
      ;;
  esac

  shift
done;

# --- Semaphore locking --------------------------------------------

LOCK=/tmp/${SEMAPHORE}.lock

if [ -f "$LOCK" ] ; then
  echo "Script is already running"
  exit 1
fi

trap "rm -f ${LOCK}" EXIT
touch $LOCK


# --- Script -------------------------------------------------------

#while read -r row ; do
#    echo "I am here."
#done < "$(tail -n +$skip_lines $input_file)"

#args="+${skip_lines} ${input_file}"
#echo $args

for line in $(tail -n +${skip_lines} ${input_file}) ; do
    # echo "$(awk -F ${delimiter})"
    arr=($(echo $line | tr ${delimiter} "\n"))
    echo "${arr[$col]}"
done
