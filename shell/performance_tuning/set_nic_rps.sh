#!/bin/bash
echo "--------------------------------------------"
echo "Receive Packet Steering"
date
mask=0
i=0
total_nic_queues=0

get_all_mask()
{
    local cpu_nums=$1
    if [ $cpu_nums -gt 32 ]; then
        mask_tail=""
        mask_low32="ffffffff"
        idx=$((cpu_nums/32))
        cpu_reset=$((cpu_nums-idx*32))

        if [ $cpu_reset -eq 0 ]; then
            mask=$mask_low32
            for((i=2;i<=idx;i++))
            do
                mask="$mask,$mask_low32"
            done
        else
            for ((i=1;i<=idx;i++))
            do
                mask_tail="$mask_tail,$mask_low32"
            done
            mask_head_num=$((2**cpu_reset-1))
            mask=`printf "%x%s" $mask_head_num $mask_tail`
        fi
    else
        mask_num=$((2**cpu_nums-1))
        mask=`printf "%x" $mask_num`
    fi

    if [ $cpu_nums -ge 32 ]; then
        echo ${mask%?}0
    else
        echo $mask
    fi
}

set_rps()
{
    if ! command -v ethtool &> /dev/null; then
        source /etc/profile
    fi

    ethtool=`which ethtool`

    cpu_nums=`cat /proc/cpuinfo |grep processor |wc -l`
    if [ $cpu_nums -eq 0 ] ;then
        exit 0
    fi


    mask=`get_all_mask $cpu_nums`
    echo "cpu number:$cpu_nums  mask:0x$mask"

    ethSet=`ls -d /sys/class/net/eth*`

    for entry in $ethSet
    do
        eth=`basename $entry`
        nic_queues=`ls -l /sys/class/net/$eth/queues/ |grep rx- |wc -l`
        if (($nic_queues==0)) ;then
            continue
        fi

        cat /proc/interrupts  | grep "LiquidIO.*rxtx" &>/dev/null
        if [ $? -ne 0 ]; then # not smartnic
            #multi queue don't set rps
            max_combined=`$ethtool -l $eth 2>/dev/null | grep -i "combined" | head -n 1 | awk '{print $2}'`
            #if ethtool -l $eth goes wrong.
            [[ ! "$max_combined" =~ ^[0-9]+$ ]] && max_combined=1
            if [ ${max_combined} -ge ${cpu_nums} ]; then
                echo "$eth has equally nic queue as cpu, don't set rps for it..."
                continue
            fi
            else
            echo "$eth is smartnic, set rps for it..."
        fi

        echo "eth:$eth  queues:$nic_queues"
        total_nic_queues=$(( $total_nic_queues+$nic_queues ))
        i=0
        while (($i < $nic_queues))  
        do
            echo "echo $mask > /sys/class/net/$eth/queues/rx-$i/rps_cpus"
            echo $mask > /sys/class/net/$eth/queues/rx-$i/rps_cpus
            if [ $cpu_nums -ge 32 ]; then
                echo 0 > /sys/class/net/$eth/queues/rx-$i/rps_flow_cnt
            else
                echo 4096 > /sys/class/net/$eth/queues/rx-$i/rps_flow_cnt
            fi
            i=$(( $i+1 )) 
        done
    done

    flow_entries=$((total_nic_queues * 4096))
    echo "total_nic_queues:$total_nic_queues  flow_entries:$flow_entries"
    echo $flow_entries > /proc/sys/net/core/rps_sock_flow_entries 
}

ethtool -l eth0

set_rps

ethtool -l eth0

