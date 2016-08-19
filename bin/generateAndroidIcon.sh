#!/bin/bash

showhelp() {
  echo "usage: $0 pngFile resDir"
}

if (( $# != 2 )); then
  showhelp
  exit 0
fi

pngFile=$1
resDir=$2

echo $pngFile
if [[ ! -f $pngFile ]]; then
  echo "$pngFile not a valid file!" >&2
  exit 1
fi
echo $resDir
if [[ ! -d $resDir ]]; then
  echo "$resDir not a valid Dir!" >&2
  exit 1
fi

if [[ ! ( -d $resDir/drawable-hdpi && -d $resDir/drawable-ldpi && -d $resDir/drawable-mdpi && -d $resDir/drawable-xhdpi ) ]]; then
  echo "drawable dir is not complete" >&2
  exit 1
fi

echo "begin scale image!"
sips -z 96 96 $pngFile -o $resDir/drawable-xhdpi/icon.png
sips -z 72 72 $pngFile -o $resDir/drawable-hdpi/icon.png
sips -z 48 48 $pngFile -o $resDir/drawable-mdpi/icon.png
sips -z 36 36 $pngFile -o $resDir/drawable-ldpi/icon.png


