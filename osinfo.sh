#!/bin/bash

# ----------------------------------------------------------------------
#
# osinfo.sh
#
# Small toolkit that reads and outputs the /etc/*release information.
#
# by Max Resing <contact@maxresing.de>
#
# ----------------------------------------------------------------------

USAGE="Usage: $0 [OPTIONS] COMMAND
Print OS information based on the os-release system information. With no
COMMAND the default command 'os' is used.

The mapping for the operating system id [/ like] is as follows:
  Alpine Linux        alpine
  Arch Linux          arch
  Debian              debian
  Kali linux          kali / debian
  Puppy Linux         puppy
  Rasbian             raspbian / debian

COMMAND:
  os            prints os-release ID
  like          prints os-release ID_LIKE with fallback to ID if missing

OPTIONS
  -h  --help    Print this help
"

COMMAND_LIST="os like"


# --- Utils ------------------------------------------------------------

function is_darwin() {
  if [[ "$(uname -s)" == "Darwin" ]] ; then
    return 0
  fi

  return 1
}

function lowercase() {
  echo "$1" | sed "y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz"
}

function strip() {
  if is_darwin; then
    echo "$1"
  else
    echo "$1" | awk -F "=" '{print $2}' | awk -F "[-_]" '{print $1}'
  fi
}

function verify_cmd() {
  if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "$USAGE"
    return 1
  fi

  verified=$(echo "$COMMAND_LIST" | grep "$1")

  if [[ -z $verified ]]; then
    echo "Invalid command: Cannot find '$1'. Use one of: $COMMAND_LIST" >> /dev/stderr
    return 1
  fi
}

# --- os ---------------------------------------------------------------
# Reads all input from /etc/*release and returns the mapping of ID=*
# Mapping as follows:
#
#
function os() {
  if is_darwin; then
    id=$(sw_vers -productName)
  else
    id=$(cat /etc/*release | grep "^ID=")
  fi
  strip "$id"
}

# --- like -------------------------------------------------------------
# Reads all input from /etc/*release and returns the mapping of ID=*
function like() {
  if is_darwin; then
    id=$(sw_vers -productName)
  else
    id=$(cat /etc/*release | grep "^ID_LIKE=")
  fi

  if [[ -z "$id" ]] ; then
    os;
  else
    strip "$id"
  fi
}

# --- Script -----------------------------------------------------------

if [[ $# == 0 ]] ; then
  os
else
  # Vefiry the input command; If valid, then just call the input.
  if verify_cmd "$1"; then
    $1
  fi
fi

