#!/bin/bash

if [[ $# -eq 0 || $1 == '-h' || $1 == '--help' ]]; then
  xtags --help
  echo "should pass filedir or file to parse"
  exit 0
fi
xtags --langmap=ObjectiveC:.m.h --languages=ObjectiveC -R "$@"
