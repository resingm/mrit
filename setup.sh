#!/bin/bash

target_dir="$HOME/bin"
mkdir -p "$target_dir"

link_file() {
  if [[ $(basename $f) == $(basename $0) ]] ; then
    return 0
  fi

  filename=$(basename $1)
  filename=${filename%.*}

  linkname="${target_dir}/${filename}"

  if [[ $1 == *.py ]] ; then
    ln -s "$f" "$linkname"
  elif [[ $1 == *.sh ]] ; then
    ln -s "$f" "$linkname"
  else
    # echo "Skip creating link for ${filename} - $1"
    :
  fi
}

for f in $(pwd)/*
do
  link_file $f
done

