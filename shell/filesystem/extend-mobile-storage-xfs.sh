#!/bin/bash
disk_name="/dev/mobile-storage/mobile-storage"
pvscan
pvresize /dev/xvdg
pvs
vgs
lvresize $disk_name -L 100000m
xfs_growfs $disk_name
df -h | grep mobile
