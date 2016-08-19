#!/bin/bash

if [[ $# -eq 0 || $1 == '-h' || $1 == '--help' ]]; then
  cat << EOF
usage $0 [-n] renamePattern files
  -n:	tryrename
  renamePattern:	a perl cmd
EOF
  exit 0
fi

if [[ $1 = "-n" ]]; then
  try=t
  shift 1
fi
cmd=$1
shift 1
for i ; do
  newName=$(perl -pe "$cmd" <<< $i)
  if [[ -z $newName ]]; then
    echo error occur 1>&2
    exit 1
  fi
  if [[ $i = $newName ]]; then
    continue
  fi
  echo "mv $i $newName"
  if [[ -z $try ]]; then
    mv $i $newName
  fi
done
