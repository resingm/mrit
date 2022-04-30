#!/usr/bin/bash

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

The mapping for the operating system ID is as follows:
  Alpine Linux        alpine
  Arch Linux          arch
  Debian              debian
  Puppy Linux         puppy_fossapup64
  Rasbian             raspbian

COMMAND:
  os            prints os-release ID
  like          prints os-release ID_LIKE with fallback to ID if missing

OPTIONS
  -h  --help    Print this help
"

COMMAND_LIST="os like"

# --- Utils ------------------------------------------------------------

function lowercase() {
  echo "$1" | sed "y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz"
}

function strip() {
  echo "$1" | awk -F "=" '{print $2}'
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
  id=$(cat /etc/*release | grep "^ID=")
  strip "$id"
}

# --- like -------------------------------------------------------------
# Reads all input from /etc/*release and returns the mapping of ID=*
# Mapping as follows:
#
#   Alpine Linux  = alpine
#   Arch Linux    = arch
#   Debian        = debian
#   Puppy Linux   = puppy_fossapup64
#   Rasbian       = raspbian
#   Ubuntu        = ubuntu
#
function like() {
  # Alpine Linux  = alpine
  # Arch Linux    = arch
  # Debian        = debian
  # Puppy Linux   = puppy_fossapup64
  # Rasbian       = debian
  # Ubuntu        = debian
  id=$(cat /etc/*release | grep "^ID_LIKE=")

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

