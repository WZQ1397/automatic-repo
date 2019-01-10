#!/bin/bash
# Func:Configure Network Bonding
# Version:2.0

trap "tput clear;tput cup 3;echo 'Any Questions: Send a message to QQ 1037509307.';tput cup 6;exit" 2 3
if [[ -n $1 ]]; then
  cat <<EOF

Network Configuration Assistant
                    --- Configure Network Bonding v1.5

Usage:

        sh $0
        chmod +x $0 && ./$0

EOF
exit 0
fi

if [[ $UID -ne 0 ]]; then
  tput clear
  tput cup 6 20
  echo -e "You must use the user: \033[31mROOT\033[0m"
  tput cup 10
  exit
fi

ERROR(){
tput cup $1 $2;tput ed
echo 'Input error,Try again pls.'
echo -e 'Press ENTER to continue..._\b\c'
read inputA
}

Check_BakFile(){
#文件备份函数
#使用方法：
#Check_BakFile 要备份的文件名 备份目录 -x(按什么时间格式备份)
case ${3} in
    -d )  #按天备份
        Bak_Date=`date '+%Y-%m-%d'`
        ;;
    -H ) #按小时备份
        Bak_Date=`date '+%Y-%m-%d_%H'`
        ;;
    -M ) #按分钟备份
        Bak_Date=`date '+%Y-%m-%d_%H:%M'`
        ;;
    -m ) #按月备份
        Bak_Date=`date '+%Y-%m'`
        ;;
    -Y ) #按年备份
        Bak_Date=`date '+%Y'`
        ;;
    * ) #默认按分钟备份
        Bak_Date=`date '+%Y-%m-%d_%H:%M'`
        ;;
esac
#Bak_Date=`date '+%Y-%m-%d-%H:%M'`

[[ -d ${2}/${Bak_Date} ]] || mkdir -p ${2}/${Bak_Date}
cp -ra ${1} ${2}/${Bak_Date}
}

bonding_pre(){
#双网卡绑定前导函数，判定网卡、IP等合法性并引导用户正确输入参数。
#全部真实网卡
NIC_NAME_all=`ifconfig -a | awk '/\<Ethernet\>/ {print $1}' | grep -wEv '^bond[0-9]+'`
#已经存在的绑定网卡
NIC_NAME_bond=`ifconfig -a | awk '/^\<bond[0-9]+\>/ {print $1}'`

#打印出已经是SLAVE的网卡
NIC_NAME_slave=`ifconfig -a | sed -n '/SLAVE/{g;1!p;};h' | awk '{print $1}'`
NIC_NAME_slave=${NIC_NAME_slave:=NULL}
#打印出可用网卡
NIC_NAME_free=`echo "$NIC_NAME_all" | grep -Fwv "$NIC_NAME_slave"`
#可用网卡数量
NIC_NAME_free_nu=`echo "$NIC_NAME_free" | wc -w`

declare -a NIC_LIST
NIC_LIST=($NIC_NAME_free)

info_print(){
tput clear;tput cup 2
cat <<EOF
----------------------------------------------
------  Network Configuration Assistant ------
----------------------------------------------
EOF
tput cup 7
if [[ -n ${1} ]]; then
  echo -e "Already existing Channel Bonding Interface of the system:\n\033[31m${1}\033[0m\n"
fi
}

if [[ "$NIC_NAME_free_nu" -gt 1 ]]; then
  info_print
  echo -e "\033[031m$NIC_NAME_free_nu\033[0m network cards available:"
  echo -e "\033[31m${NIC_LIST[@]}\033[0m"
  echo -e "----------------------------------------------\n"
  #输入第一块网卡的名称
  while true; do
    echo -e "\nPlease enter the First NIC:_\b\c"
    read NIC1
    echo ${NIC_LIST[@]} | grep -Fw "$NIC1" &> /dev/null
    if [[ $? -eq 0 ]]; then
      info_print
      echo -e "\033[031m$NIC_NAME_free_nu\033[0m network cards available:\n\033[31m${NIC_LIST[@]}\033[0m"
      echo -e "\nThe information you have entered:\nFirst NIC     : $NIC1"
      echo -e "----------------------------------------------\n"
      break
    else
      info_print
      echo -e "\033[031m$NIC_NAME_free_nu\033[0m network cards available:\n\033[31m${NIC_LIST[@]}\033[0m"
      echo -e "----------------------------------------------\n"
      echo -e "\033[31m${NIC1}\033[0m is not available,Please enter another one."
    fi
  done
  #输入第二块网卡的名称
  while true; do
    echo -e "\nPlease select the second NIC:_\b\c"
    read NIC2
    if [[ ${NIC1} != ${NIC2} ]]; then
      echo ${NIC_LIST[@]} | grep -Fw "${NIC2}" &> /dev/null
      if [[ $? -eq 0 ]]; then
        info_print "${NIC_NAME_bond}"
        echo -e "The information you have entered:\nFirst NIC     : ${NIC1}\nSecond NIC    : ${NIC2}"
        echo -e "----------------------------------------------\n"
        break
      else
        info_print
        echo -e "\033[031m$NIC_NAME_free_nu\033[0m network cards available:\n\033[31m${NIC_LIST[@]}\033[0m\n\nThe information you have entered:\nFirst NIC     : ${NIC1}"
        echo -e "----------------------------------------------\n"
        echo -e "\033[31m${NIC2}\033[0m is not available,Please enter another one."
      fi
    else
      info_print
      echo -e "\033[031m${NIC_NAME_free_nu}\033[0m network cards available:\n\033[31m${NIC_LIST[@]}\033[0m\n\nThe information you have entered:\nFirst NIC     : ${NIC1}"
      echo -e "----------------------------------------------\n"
      echo -e "\033[31m${NIC2}\033[0m is the first NIC,Please enter another one."
    fi
  done

  #输入绑定网卡名称并进行合理性检查
  if [[ -z ${NIC_NAME_bond} ]]; then
    NAME_bond=bond0
    info_print
    echo -e "The information you have entered:\nFirst NIC     : ${NIC1}\nSecond NIC    : ${NIC2}\nbond name     : ${NAME_bond}"
    echo -e "----------------------------------------------\n"
    echo "The default first bond name is -- bond0."
  else
    while true; do
      echo -e "\nPlease enter a bond name[bonN]:_\b\c"
      read NAME_bond
      #检查输入格式是否为bond+数字的格式。
      echo "${NAME_bond}" | grep -wE '^bond[[:digit:]]+$' &> /dev/null
      if [[ $? -eq 0 ]]; then
        echo "${NIC_NAME_bond}" | grep -Fw "${NAME_bond}" &> /dev/null
        if [[ $? -ne 0 ]]; then
          info_print "${NIC_NAME_bond}"
          echo -e "The information you have entered:\nFirst NIC     : ${NIC1}\nSecond NIC    : ${NIC2}\nbond name     : ${NAME_bond}"
          echo -e "----------------------------------------------\n"
          break
        else
          info_print "${NIC_NAME_bond}"
          echo -e "The information you have entered:\nFirst NIC     : ${NIC1}\nSecond NIC    : ${NIC2}"
          echo -e "----------------------------------------------\n"
          echo "You can not use an existing name: ${NAME_bond}"
          echo -e "\033[31m${NAME_bond}\033[0m is not available,Please enter another one like -- bondN."
        fi
      else
        info_print "${NIC_NAME_bond}"
        echo -e "The information you have entered:\nFirst NIC     : ${NIC1}\nSecond NIC    : ${NIC2}"
        echo -e "----------------------------------------------\n"
        echo -e "\033[31m${NAME_bond}\033[0m is not available,Please enter another one like -- bondN."
      fi
    done
  fi

  #设置IP地址
  while true; do
    echo -e "\nPlease enter an IP address:_\b\c"
    read IP_bond
    echo "${IP_bond}" | grep -owE '^(([1-9]|[1-9][0-9]|1[0-9]{2}|2[0-5]{2})\.){3}([1-9]|[1-9][0-9]|1[0-9]{2}|2[0-5]{2})$' &> /dev/null
    if [[ $? -eq 0 ]]; then
      info_print
      echo -e "The information you have entered:\nFirst NIC     : ${NIC1}\nSecond NIC    : ${NIC2}\nbond name     : ${NAME_bond}\nIP address    : ${IP_bond}"
      echo -e "----------------------------------------------\n"
      break
    else
      info_print
      echo -e "The information you have entered:\nFirst NIC     : ${NIC1}\nSecond NIC    : ${NIC2}\nbond name     : ${NAME_bond}"
      echo -e "----------------------------------------------\n"
      echo -e "IP address: \033[31m${IP_bond}\033[0m format errors, please re-enter."
    fi
  done
  #设置netmask
  while true; do
    echo -e "\nPls enter the NETMASK[255.255.255.0]:_\b\c"
    read NETMASK_bond
    NETMASK_bond=${NETMASK_bond:="255.255.255.0"}   #当变量为NETMASK_bond为空时，给其赋默认值255.255.255.0
    echo "$NETMASK_bond" | grep -owE  '^(128|192|224|240|248|252|254|255)\.((0|128|192|224|240|248|252|254|255)\.){2}(0|128|192|224|240|248|252|254|255)$' &> /dev/null
    if [[ $? -eq 0 ]]; then
      info_print
      echo -e "The information you have entered:\nFirst NIC     : ${NIC1}\nSecond NIC    : ${NIC2}\nbond name     : ${NAME_bond}\nIP address    : ${IP_bond}\nnetmask       : ${NETMASK_bond}"
      echo -e "----------------------------------------------\n"
      break
    else
      info_print
      echo -e "The information you have entered:\nFirst NIC     : ${NIC1}\nSecond NIC    : ${NIC2}\nbond name     : ${NAME_bond}\nIP address    : ${IP_bond}"
      echo -e "----------------------------------------------\n"
      echo -e "Input error.\nPlease enter the correct NETMASK or press ENTER to use 255.255.255.0.\n"
    fi
  done
#:<<!zhushi!  #批量注释，如果开启批量注释，默认mode=1
  while true; do
    echo -e "\nPls enter the bonding_mode[default:mode=1,active-backup]:_\b\c"
    read mode_bond
    mode_bond=${mode_bond:="mode=1"}   #当变量为mode_bond为空时，给其赋默认值1
    if [[ ! ${mode_bond} =~ "mode=[0-6]" ]]; then
      info_print
      echo -e "The information you have entered:\nFirst NIC     : ${NIC1}\nSecond NIC    : ${NIC2}\nbond name     : ${NAME_bond}\nIP address    : ${IP_bond}\netmask       : ${NETMASK_bond}"
      echo -e "----------------------------------------------\n"
      echo "Invalid answer: ${mode_bond}"
      echo "Eg: mode={0,1,2,3,4,5,6}"
    else
      info_print
      echo -e "The information you have entered:\n"
      echo -e "First NIC     :${NIC1}\nSecond NIC    :${NIC2}\nbond name     :${NAME_bond}\nIP address    :${IP_bond}\nnetmask       :${NETMASK_bond}\nbonding_mode  :${mode_bond}"
      echo -e "----------------------------------------------\n"
      break
    fi
  done
#!zhushi!

  #选择是否设置primary网卡
  while true; do
    echo "1-${NIC1}"
    echo "2-${NIC2}"
    echo "3-none"
    echo -e "choose whether to set up the primary NIC or not[default:3-none]:_\b\c"
    read get_primary_NIC
    get_primary_NIC=${get_primary_NIC:="none"}
        case ${get_primary_NIC} in
        1 )
          get_primary_NIC=${NIC1}
          #echo "--$get_primary_NIC"
          break
          ;;
        2 )
          get_primary_NIC=${NIC2}
            #echo "--$get_primary_NIC"
          break
          ;;
        3 )
          get_primary_NIC=none
            #echo "--$get_primary_NIC"
          break
          ;;
        none )
          break
          ;;
        * )
            #echo "--$get_primary_NIC"
          info_print
          echo -e "The information you have entered:\nFirst NIC     : ${NIC1}\nSecond NIC    : ${NIC2}\nbond name     : ${NAME_bond}\nIP address    : ${IP_bond}\nnetmask       : ${NETMASK_bond}"
          echo -e "----------------------------------------------\n"
          echo "Invalid answer: ${get_primary_NIC}"
          echo "Pls input a number in {1,2,3} or press ENTER to set up primary NIC none."
          continue
          ;;
      esac

      info_print
      echo -e "The information you have entered:\n"
      echo -e "First NIC     :${NIC1}\nSecond NIC    :${NIC2}\nbond name     :${NAME_bond}\nIP address    :${IP_bond}\nnetmask       :${NETMASK_bond}\nbonding_mode  :${mode_bond}\nprimary NIC   :${get_primary_NIC}"
      echo -e "----------------------------------------------\n"
      break
  done

  #最终输入信息确认
  while true; do
    info_print
    echo -e "The information you have entered:\n"
    echo -e "\033[31mFirst NIC     :${NIC1}\nSecond NIC    :${NIC2}\nbond name     :${NAME_bond}\nIP address    :${IP_bond}\nnetmask       :${NETMASK_bond}\nbonding_mode  :${mode_bond}\nprimary NIC   :${get_primary_NIC}\033[0m"
    echo -e "----------------------------------------------\n"
    echo -e "Pls make sure its OK[y/n]:_\b\c"
    read input
    case ${input} in
      [Yy]|[Yy][Ee][Ss] )
        bonding "$NIC1" "$NIC2" "$NAME_bond" "$IP_bond" "$NETMASK_bond"
        break
        ;;
      [Nn]|[Nn][Oo] )
        bonding_pre
      ;;
      * )
        tput cup 7;tput ed
        ERROR 7 10
      ;;
    esac
  done
else
    info_print
    echo -e "You have \033[031m${NIC_NAME_free_nu}\033[0m network cards available:\n"
    #将重点显示的“网卡名”标示为红色
    echo -e "\033[31m${NIC_LIST[@]}\033[0m\n"
    echo -e "There are \033[31mnot enough\033[0m network cards to make bonding"
    echo -e "Pls check it......\n"
    echo -e 'Press ENTER to exit..._\b\c'
    read answer
    exit 1
fi
}

bonding(){
if [[ $# -lt 5 ]]
then
  echo 'Bonding failed! Please provide enough information!'
  echo -e "\nUsage:\n       sh bonding.sh <NIC1_name> <NIC2_name> <bond_name> <IP> <NETMASK>\n\n"
  exit 1
fi
#get device name and ip information
SLAVE1_DEV="$1"       #SLAVE1_DEV=ethx
SLAVE2_DEV="$2"       #SLAVE2_DEV=ethx
BOND_DEV="$3"         #BOND_DEV=bondx
SLAVE1=ifcfg-"$1"
SLAVE2=ifcfg-"$2"
BOND=ifcfg-"$3"
BOND_IPADDR="$4"
BOND_NETMASK="$5"
BOND_DIR=/etc/sysconfig/network-scripts
if [ -e $BOND_DIR/$BOND ]
then
  echo $BOND_DIR/$BOND is already exist
else
  #file backup
  Check_BakFile "${BOND_DIR}/ifcfg-*" "${BOND_DIR}/inspur_bak" "-M"

#get mac address
  SLAVE1_MAC=`grep 'HWADDR' ${BOND_DIR}/${SLAVE1}`
  SLAVE2_MAC=`grep 'HWADDR' ${BOND_DIR}/${SLAVE2}`

  # modify $BOND
  touch $BOND_DIR/$BOND
  echo "DEVICE=${BOND_DEV}" >> $BOND_DIR/$BOND
  echo "BOOTPROTO=none" >> $BOND_DIR/$BOND
  echo "ONBOOT=yes" >> $BOND_DIR/$BOND
  echo "TYPE=Ethernet" >> $BOND_DIR/$BOND
  echo "USERCTL=no" >> $BOND_DIR/$BOND
  echo "IPV6INIT=no" >> $BOND_DIR/$BOND
  echo "PEERDNS=yes" >> $BOND_DIR/$BOND
  echo "IPADDR=${BOND_IPADDR}" >> $BOND_DIR/$BOND
  echo "NETMASK=${BOND_NETMASK}" >> $BOND_DIR/$BOND
  if [[ ${get_primary_NIC} == none ]]; then
      echo "BONDING_OPTS=\"miimon=100 ${mode_bond}\"" >> $BOND_DIR/$BOND
  else
      echo "BONDING_OPTS=\"miimon=100 ${mode_bond} primary=$(echo ${SLAVE1} | cut -d'-' -f2)\"" >> $BOND_DIR/$BOND
  fi

  # modify $SLAVE1
  > $BOND_DIR/$SLAVE1
  echo "DEVICE=${SLAVE1_DEV}" >> $BOND_DIR/$SLAVE1
  echo 'BOOTPROTO=none' >> $BOND_DIR/$SLAVE1
  #cat $BOND_DIR/../ifcfg-bak/$SLAVE1 |grep HWADDR >> $BOND_DIR/$SLAVE1
  echo "#$SLAVE1_MAC" >> $BOND_DIR/$SLAVE1
  echo ONBOOT=yes >> $BOND_DIR/$SLAVE1
  echo TYPE=Ethernet >> $BOND_DIR/$SLAVE1
  echo USERCTL=no >> $BOND_DIR/$SLAVE1
  echo IPV6INIT=no >> $BOND_DIR/$SLAVE1
  echo PEERDNS=yes >> $BOND_DIR/$SLAVE1
  echo SLAVE=yes >> $BOND_DIR/$SLAVE1
  echo MASTER=$BOND_DEV >> $BOND_DIR/$SLAVE1

  # modify SLAVE2
  > $BOND_DIR/$SLAVE2
  echo "DEVICE=$SLAVE2_DEV" >> $BOND_DIR/$SLAVE2
  echo BOOTPROTO=none >> $BOND_DIR/$SLAVE2
  #cat $BOND_DIR/../ifcfg-bak/$SLAVE2 |grep HWADDR >> $BOND_DIR/$SLAVE2
  echo "#$SLAVE2_MAC" >> $BOND_DIR/$SLAVE2
  echo ONBOOT=yes >> $BOND_DIR/$SLAVE2
  echo TYPE=Ethernet >> $BOND_DIR/$SLAVE2
  echo USERCTL=no >> $BOND_DIR/$SLAVE2
  echo IPV6INIT=no >> $BOND_DIR/$SLAVE2
  echo PEERDNS=yes >> $BOND_DIR/$SLAVE2
  echo SLAVE=yes >> $BOND_DIR/$SLAVE2
  echo MASTER=$BOND_DEV >> $BOND_DIR/$SLAVE2

  [[ -e /etc/modprobe.conf.bak ]] && cp /etc/modprobe.conf /etc/modprobe.conf.bak.new || cp /etc/modprobe.conf /etc/modprobe.conf.bak
  echo "alias $BOND_DEV bonding" >> /etc/modprobe.conf

while true; do
  tput clear;tput cup 2
cat <<EOF
----------------------------------------------
------  Network Configuration Assistant ------
----------------------------------------------

Complete!
File backup directory: ${BOND_DIR}/inspur_bak

you can check the file and then restart the network service.

1 ) service network restart
2 ) exit
----------------------------------------------
EOF
    echo -e "Please make your choice:_\b\c"
    read answer
      case ${answer} in
        1 )
          service network restart
          exit 0
          ;;
        2 )
          exit 0
          ;;
      esac

  done
fi
}

main(){
  while true; do
    bonding_pre
  done
}

main