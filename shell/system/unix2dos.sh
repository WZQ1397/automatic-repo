#!/usr/bin/env bash

progname=${0##*/}
CR=$(printf "\r")
tempfile=$(mktemp $progname.XXX) || exit 5

for file 
do
   sed -e "s/$/$CR/" -e "s/$CR$CR$/$CR/" "$file" > "$tempfile" &&
   mv "$tempfile" "$file"
done