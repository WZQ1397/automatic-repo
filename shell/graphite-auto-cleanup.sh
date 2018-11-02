#!/bin/bash

# The graphite directory to monitoring
dir=$1
# The timeout to remove the data
timeout=$2

find $dir -type f -mtime +$timeout -name \*.wsp -delete; find $dir -depth -type d -empty -delete