#!/bin/bash
#
# Script to check MegaRaidCLI status and Critical/Failed drives
#
# Example:
#   ------------------------------------
#   Extra options: ./MegaRAID_SUM --help
#   ------------------------------------
#   
#                   Device Present
#                   ================
#   Virtual Drives    : 16
#     Degraded        : 0
#     Offline         : 2
#   Physical Devices  : 19
#     Disks           : 17
#     Critical Disks  : 0
#     Failed Disks    : 2
#   
#   
#   Virtual Drive: 0  | RAIDlvl: 1 | #Drives: 2 | State: Optimal | Span Ref: 00 | Size: 278.0 GB
#   Virtual Drive: 1  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 01 | Size: 2.727 TB
#   Virtual Drive: 2  | RAIDlvl: 0 | #Drives: 1 | State: Offline | Span Ref: 02 | Size: 2.727 TB
#   Virtual Drive: 3  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 03 | Size: 2.727 TB
#   Virtual Drive: 4  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 04 | Size: 2.727 TB
#   Virtual Drive: 5  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 05 | Size: 2.727 TB
#   Virtual Drive: 6  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 06 | Size: 2.727 TB
#   Virtual Drive: 7  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 07 | Size: 2.727 TB
#   Virtual Drive: 8  | RAIDlvl: 0 | #Drives: 1 | State: Offline | Span Ref: 08 | Size: 3.637 TB
#   Virtual Drive: 9  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 09 | Size: 2.727 TB
#   Virtual Drive: 10  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 0a | Size: 2.727 TB
#   Virtual Drive: 16  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 0b | Size: 2.727 TB
#   Virtual Drive: 11  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 0c | Size: 3.637 TB
#   Virtual Drive: 12  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 0d | Size: 3.637 TB
#   Virtual Drive: 14  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 0e | Size: 3.637 TB
#   Virtual Drive: 15  | RAIDlvl: 0 | #Drives: 1 | State: Optimal | Span Ref: 0f | Size: 2.727 TB
#   
#   Slot: 0 - Drive's position: DiskGroup: 1, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 1 - Drive's position: DiskGroup: 2, Span: 0, Arm: 0 -  Failed
#   Slot: 2 - Drive's position: DiskGroup: 3, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 3 - Drive's position: DiskGroup: 4, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 4 - Drive's position: DiskGroup: 5, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 5 - Drive's position: DiskGroup: 6, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 6 - Drive's position: DiskGroup: 7, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 7 - Drive's position: DiskGroup: 8, Span: 0, Arm: 0 -  Failed
#   Slot: 8 - Drive's position: DiskGroup: 9, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 9 - Drive's position: DiskGroup: 10, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 10 - Drive's position: DiskGroup: 12, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 11 - Drive's position: DiskGroup: 13, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 13 - Drive's position: DiskGroup: 14, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 14 - Drive's position: DiskGroup: 15, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 15 - Drive's position: DiskGroup: 11, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 0 - Drive's position: DiskGroup: 0, Span: 0, Arm: 0 -  Online, Spun Up
#   Slot: 1 - Drive's position: DiskGroup: 0, Span: 0, Arm: 1 -  Online, Spun Up
#

Replace_failed(){
  faild=$(sudo /opt/MegaRAID/MegaCli/MegaCli64 -PDList -aALL | /bin/egrep "Failed" | wc -l)

  if [ "$faild" -ge 1 ]; then
    sudo /opt/MegaRAID/MegaCli/MegaCli64 -CfgDsply -aALL > Cfgdsply-text
    mapfile -t failed_line < <( cat Cfgdsply-text | /bin/egrep -n "Failed" | cut -d':' -f1 )

    for (( i = 0; i < ${#failed_line[@]}; i++))
    do
      sed -n "1,${failed_line[$i]}p" Cfgdsply-text > Cfgdsply-tofailed-text
      tac Cfgdsply-tofailed-text > backw-Cfgdsplytext
      fadpt=$(/bin/egrep -m 1 "Adapter" backw-Cfgdsplytext | cut -d':' -f2 | sed -e "s/ //g")
      enclID=$(/bin/egrep -m 1 "Enclosure Device ID" backw-Cfgdsplytext | cut -d':' -f2 | sed -e "s/ //g")
      slot=$(/bin/egrep -m 1 "Slot Number" backw-Cfgdsplytext | cut -d':' -f2 | sed -e "s/ //g")
      spanref=$(/bin/egrep -m 1 "Span Reference" backw-Cfgdsplytext | cut -d':' -f2 | sed -e "s/ //g" | cut -d'x' -f2 | cut -c 2)
      row=$(/bin/egrep -m 1 "Physical Disk:" backw-Cfgdsplytext | cut -d':' -f2 | sed -e "s/ //g")
 
      echo "Replace Drive at: adapter: # $fadpt - enclID: $enclID - slot: $slot | Span ref: $spanref | Row: $row ??"
      echo "(yes) or (no)"
      read REPLACE

      if [ "$REPLACE" == "yes" ]; then
        echo "Setting disk offline..."
        sudo /opt/MegaRAID/MegaCli/MegaCli64 -pdoffline -physdrv[$enclID:$slot] -a$fadpt
        echo "Marking disk as missing..."
        sudo /opt/MegaRAID/MegaCli/MegaCli64 -pdmarkmissing -physdrv[$enclID:$slot] -a$fadpt
        echo "Preparing for removal..."
        sudo /opt/MegaRAID/MegaCli/MegaCli64 -pdprprmv -physdrv[$enclID:$slot] -a$fadpt
        echo
        echo "Replace disk now..."
        echo "Done? (yes) or (no)"
        read DONE
        if [ "$DONE" == “yes” ]; then
          echo "Replace missing and start rebuilding..."
          sudo /opt/MegaRAID/MegaCli/MegaCli64 -PdReplaceMissing -PhysDrv[$enclID:$slot] -Array$spanref -row$row -a$fadpt
          sudo /opt/MegaRAID/MegaCli/MegaCli64 -PDRbld -Start -PhysDrv [$enclID:$slot] -a$fadpt
        else
          exit
        fi
      else
        continue
      fi
    done

    # temp file clean-up
    rm -f Cfgdsply-text
    rm -f Cfgdsply-tofailed-text
    rm -f backw-Cfgdsplytext

  else
    echo "No Failed drives"
  fi
}

Show_failed(){
  faild=$(sudo /opt/MegaRAID/MegaCli/MegaCli64 -PDList -aALL | /bin/egrep "Failed" | wc -l)

  if [ "$faild" -ge 1 ]; then
    sudo /opt/MegaRAID/MegaCli/MegaCli64 -CfgDsply -aALL > Cfgdsply-text
    mapfile -t failed_line < <( cat Cfgdsply-text | /bin/egrep -n "Failed" | cut -d':' -f1 )

    for (( i = 0; i < ${#failed_line[@]}; i++))
    do
      sed -n "1,${failed_line[$i]}p" Cfgdsply-text > Cfgdsply-tofailed-text
      tac Cfgdsply-tofailed-text > backw-Cfgdsplytext
      fadpt=$(/bin/egrep -m 1 "Adapter" backw-Cfgdsplytext | cut -d':' -f2 | sed -e "s/ //g")
      enclID=$(/bin/egrep -m 1 "Enclosure Device ID" backw-Cfgdsplytext | cut -d':' -f2 | sed -e "s/ //g")
      slot=$(/bin/egrep -m 1 "Slot Number" backw-Cfgdsplytext | cut -d':' -f2 | sed -e "s/ //g")
      spanref=$(/bin/egrep -m 1 "Span Reference" backw-Cfgdsplytext | cut -d':' -f2 | sed -e "s/ //g" | cut -d'x' -f2 | cut -c 2)
      row=$(/bin/egrep -m 1 "Physical Disk:" backw-Cfgdsplytext | cut -d':' -f2 | sed -e "s/ //g")

      echo "Failed at:"
      echo "   adapter: # $fadpt - enclID: $enclID - slot: $slot | Span ref: $spanref | Row: $row"
      echo

      echo "Start blinking LED on drives?(start) or Stop blinking (stop)"
      read STARTB

      if [ "$STARTB" == "start" ]; then
        echo "sudo /opt/MegaRAID/MegaCli/MegaCli64 -PdLocate -start -physdrv \[$enclID:$slot\]  -a$fadpt"
        sudo /opt/MegaRAID/MegaCli/MegaCli64 -PdLocate -start -physdrv \[$enclID:$slot\]  -a$fadpt

      elif [ "$STARTB" == "stop" ]; then
        echo "sudo /opt/MegaRAID/MegaCli/MegaCli64 -PdLocate -stop -physdrv \[$enclID:$slot\]  -a$fdapt"
        sudo /opt/MegaRAID/MegaCli/MegaCli64 -PdLocate -stop -physdrv \[$enclID:$slot\]  -a$fdapt
      else
        continue
      fi
    done

    # temp file clean-up
    rm -f Cfgdsply-text
    rm -f Cfgdsply-tofailed-text
    rm -f backw-Cfgdsplytext

  else
    echo "No Failed drives"
  fi
}

arg=$1

case $arg in
  -h|--help)
    echo "-h        show options"
    echo "-a        show all MegaRAID info"
    echo "-p        show physical drives info "
    echo "-v        show virtual drive & physical info"
    echo "-f        show failed drive info"
    echo "-r        replace failed drive"
    ;;
  -a)
    sudo /opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aAll | less
    ;;
  -p)
    sudo /opt/MegaRAID/MegaCli/MegaCli64 -PDList -aALL | less
    ;;
  -v)
    sudo /opt/MegaRAID/MegaCli/MegaCli64 -CfgDsply -aALL | less
    ;;
  -f)
    Show_failed
    ;;
  -r)
    Replace_failed
  ;;
esac

if [ $# -eq 0 ]; then
  echo "------------------------------------"
  echo "Extra options: ${0} --help"
  echo "------------------------------------"
  echo
  
  sudo /opt/MegaRAID/MegaCli/MegaCli64 -AdpAllInfo -aAll > Adpallinfo-text
  sudo /opt/MegaRAID/MegaCli/MegaCli64 -CfgDsply -aALL > Cfgdsply-text
  sudo /opt/MegaRAID/MegaCli/MegaCli64 -PDList -aALL > Pdlist-text
  
  degrade=$(cat Adpallinfo-text | /bin/egrep 'Degrade' | awk '/[0-9]/ {print $3}')
  offline=$(cat Adpallinfo-text | /bin/egrep '[[:space:]][[:space:]]Offline' | awk '/[0-9]/ {print $3}')
  critical=$(cat Adpallinfo-text | /bin/egrep 'Critical' | awk '/[0-9]/ {print $4}')
  failed=$(cat Adpallinfo-text | /bin/egrep '[[:space:]][[:space:]]Failed' | awk '/[0-9]/ {print $4}')
  
  mapfile -t VIRTdrives < <(cat Cfgdsply-text | /bin/egrep 'Virtual Drive:'| cut -d'(' -f1)
  mapfile -t RAIDlvl < <(cat Cfgdsply-text | /bin/egrep 'RAID Level' | awk ' {print $4}'| cut -d'-' -f2 | cut -c1)
  mapfile -t drivenum < <(cat Cfgdsply-text | /bin/egrep 'Drives' | cut -d':' -f2)
  mapfile -t RAIDstate < <(cat Cfgdsply-text | /bin/egrep 'State\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s' | cut -d':' -f2)
  mapfile -t RAIDsize < <(cat Cfgdsply-text | /bin/egrep 'Size\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s:'| cut -d':' -f2)
  mapfile -t SPANref < <(cat Cfgdsply-text | /bin/egrep 'Span Reference' | cut -d':' -f2 | cut -d'x' -f2)
  
  cat Adpallinfo-text | /bin/egrep -A 9 'Device Present'
  echo
  
  for (( i = 0;  i < ${#VIRTdrives[@]}; i++))
  do
    echo "${VIRTdrives[$i]} | RAIDlvl: ${RAIDlvl[$i]} | #Drives:${drivenum[$i]} | State:${RAIDstate[$i]} | Span Ref: ${SPANref[$i]} | Size:${RAIDsize[$i]}"
  done
  
  mapfile -t slotnum < <(cat Pdlist-text | /bin/grep 'Slot Number'| cut -d':' -f2 | cut -c2-3)
  mapfile -t firmstate < <(cat Pdlist-text | /bin/grep "Firmware state" | cut -d':' -f2)
  mapfile -t position < <(cat Pdlist-text | /bin/grep "Drive's position" | cut -f2,4)
  echo
  for (( i = 0; i < ${#slotnum[@]}; i++))
  do
    echo "Slot: ${slotnum[$i]} - ${position[$i]} - ${firmstate[$i]}"
  done
  
  # Clean up temp files
  rm -f Adpallinfo-text
  rm -f Cfgdsply-text
  rm -f Pdlist-text
fi