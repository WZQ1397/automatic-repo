#!/bin/bash
#########################################################################
# File Name: XenServer_Add_ISO.sh
#########################################################################
 
#ColorAuto================================================================
echo=echo
for cmd in echo /bin/echo; do
    $cmd >/dev/null 2>&1 || continue
    if ! $cmd -e "" | grep -qE '^-e'; then echo=$cmd && break; fi
done
CSI=$($echo -e "\033[")
CEND="${CSI}0m"
CDGREEN="${CSI}32m"
CRED="${CSI}1;31m"
CGREEN="${CSI}1;32m"
CYELLOW="${CSI}1;33m"
CBLUE="${CSI}1;34m"
CMAGENTA="${CSI}1;35m"
CCYAN="${CSI}1;36m"
CQUESTION="$CMAGENTA"
CWARNING="$CRED"
CMSG="$CCYAN"
 
VG_Name=`vgs 2>/dev/null|awk '/VG_XenStorage/{print $1}'`
 
echo "${CGREEN}Pls input your ISO Storage name: ${CEND}"
read -p "Name: " iso_storage
echo "${CGREEN}Pls input your ISO Storage Space: ${CEND}"
read -p "Space: " iso_space
 
lvcreate -L ${iso_space} -n ${iso_storage} ${VG_Name}
modprobe dm-mod >/dev/null 2>&1
vgscan >/dev/null 2>&1
vgchange -ay >/dev/null 2>&1
mkfs.ext3 /dev/${VG_Name}/${iso_storage}
mkdir -p /${iso_storage}
echo -e "$(blkid /dev/${VG_Name}/${iso_storage} |awk '{print $2}')\t/${iso_storage}\text3\tdefaults\t0 0" >> /etc/fstab
mount -a
xe sr-create name-label=iso_storage type=iso device-config:location=/${iso_storage} device-config:legacy_mode=true content-type=iso
echo "${CWARNING}Done !${CEND}"