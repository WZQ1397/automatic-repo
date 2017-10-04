#!/bin/bash
#
# Check All IPMI Sensors
#

if $(grep -Eq 'flags.*hypervisor' /proc/cpuinfo); then
  echo "OK. This is a virtual machine"
  exit 0
fi

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

ipmitool_bin=$(which ipmitool 2> /dev/null)
if [[ $? -ne 0 ]]; then
  echo "ERROR: No such ipmitool command, try 'yum install ipmitool'."
  exit 2
fi

ipmi_sensor_list=$(${ipmitool_bin} sensor list | grep -v 'command failed' | awk -F '|' '{print $1"|"$2"|"$3"|"$4"|"}' | sed -e 's/ *| */|/g' -e 's/ /_/g' | grep -Evw 'ns|nc|na|discrete')
ipmi_sensor_count=$(echo ${ipmi_sensor_list} | xargs -n 1 | wc -l)
for ipmi_sensor_item in ${ipmi_sensor_list}; do
  ipmi_sensor_name=$(echo ${ipmi_sensor_item} | cut -d'|' -f1)
  ipmi_sensor_value=$(echo ${ipmi_sensor_item} | cut -d'|' -f2)
  ipmi_sensor_unit=$(echo ${ipmi_sensor_item} | cut -d'|' -f3)
  ipmi_sensor_status=$(echo ${ipmi_sensor_item} | cut -d'|' -f4)
  if [[ ${ipmi_sensor_status} != 'ok' ]]; then
    if [[ -z "${crit_msg}" ]]; then
      crit_msg="${ipmi_sensor_name} is ${ipmi_sensor_value} ${ipmi_sensor_unit}"
    else
      crit_msg="${crit_msg}, ${ipmi_sensor_name} is ${ipmi_sensor_value} ${ipmi_sensor_unit}"
    fi
  fi
done

if [[ -z "${crit_msg}" ]]; then
  echo "OK. All ${ipmi_sensor_count} Sensors are OK"
  exit 0
else
  echo "CRIT. ${crit_msg}"
  exit 2
fi