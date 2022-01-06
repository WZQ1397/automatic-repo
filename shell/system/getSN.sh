#Author: zach.wang
# apt install -y dmidecode lshw smartmontools
randomfile=`cat /dev/urandom | od -x  | head -c 48 | sed -e "s/0\{5,\}//g" -e "s/ //g"`

echo "BIOS"
dmidecode -t 2 | grep Serial | awk '{print $NF}' | tee -a $randomfile
echo "NIC"
#lshw -c network | grep serial | head -n 1 | awk '{print $NF}' | tee -a $randomfile
#lshw -c network | grep -A 2 -E "logical name: en|logical name: eth" | grep "serial:" | awk '{print $NF}'
ip a | grep -A 2 -E " eno| enp| enx| ens| eth" | grep "link/ether" | awk '{print $2}'
echo "CPU"
dmidecode -t 4 | grep ID | sed -e "s/ID://g" -e "s/\t//g"| uniq | tee -a $randomfile
echo "OEM uuid"
dmidecode –t 11 | grep -i uuid |  awk '{print $NF}' | tee -a $randomfile
echo "GPU uuid"
nvidia-smi --query-gpu=name,uuid --format=csv,noheader | tee -a $randomfile
echo "DISK SN"
for disk in /dev/sd[a-z]; do echo "DISK $disk SN:"; smartctl -i $disk | grep "Serial Number" | awk '{print $NF}' | tee -a $randomfile; done
echo "======================== hardcode ========================="
sha512sum  $randomfile | cut -d ' ' -f 1 | tee hdcode.txt
