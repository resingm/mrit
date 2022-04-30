#!/usr/bin/bash

# ----------------------------------------------------------------------
#
# 
#
# by Max Resing <contact@maxresing.de>
#
# ----------------------------------------------------------------------

USAGE="Usage: $0 COMMAND
Print OS information based on the os-release system information. With no
COMMAND this output is printed.

The mapping for the operating system ID is as follows:
  Alpine Linux        alpine
  Arch Linux          arch
  Debian              debian
  Puppy Linux         puppy_fossapup64
  Rasbian             raspbian

Commands:
  id          prints os-release ID
  like        prints os-release ID_LIKE with fallback to ID if missing
"

# --- Utils ------------------------------------------------------------

function lowercase() {
  echo "$1" | sed "y/ABCDEFGHIJKLMNOPQRSTUVWXYZ/abcdefghijklmnopqrstuvwxyz"
}

function strip() {
  echo "$1" | awk -F "=" '{print $2}'
}

# --- id ---------------------------------------------------------------
# Reads all input from /etc/*release and returns the mapping of ID=*
# Mapping as follows:
#
#
function id() {
  _id=$(cat /etc/*release | grep "^ID=")
  strip "$_id"
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
    id;
  else
    strip "$id"
  fi
}

# --- Script -----------------------------------------------------------

if [[ $# == 0 ]] ; then
  echo "$USAGE"
else
  $1
fi

