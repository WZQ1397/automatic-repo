#!/bin/bash
##used to bind virtio-input interrupt to last cpu
PATH=$PATH:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
dir=$(cd `dirname $0`;pwd)

echo "--------------------------------------------"
date

get_highest_mask()
{
    cpu_nums=$1
    if [ $cpu_nums -gt 32 ]; then
        mask_tail=""
        mask_low32="00000000"
        idx=$((cpu_nums/32))
        cpu_reset=$((cpu_nums-idx*32))

        if [ $cpu_reset -eq 0 ]; then
            mask="80000000"
            for((i=2;i<=idx;i++))
            do
                mask="$mask,$mask_low32"
            done
        else
            for ((i=1;i<=idx;i++))
            do
                mask_tail="$mask_tail,$mask_low32"
            done
            mask_head_num=$((1<<(cpu_reset-1)))
            mask=`printf "%x%s" $mask_head_num $mask_tail`
        fi

    else
        mask_num=$((1<<(cpu_nums-1)))
        mask=`printf "%x" $mask_num`
    fi
    echo $mask
}

get_smp_affinity_mask()
{
    local cpuNums=$1

    if [ $cpuNums -gt $gCpuCount ]; then
        cpuNums=$(((cpuNums - 1) % gCpuCount + 1))
    fi

    if [ $gReverse == 1 ];then
        cpuNums=$((gCpuCount + 1 - cpuNums))
    fi

    get_highest_mask $cpuNums
}

input_irq_bind()
{
    netQueueCount=`cat /proc/interrupts  | grep -i ".*virtio.*input.*" | wc -l`
    irqSet=`cat /proc/interrupts  | grep -i ".*virtio.*input.*" | awk -F ':' '{print $1}'`
    i=0
    for irq in $irqSet
    do
        cpunum=$((i%gCpuCount+1))
        mask=`get_smp_affinity_mask $cpunum`
        echo $mask > /proc/irq/$irq/smp_affinity
        echo "[input]bind irq $irq with mask 0x$mask affinity"
        ((i++))
    done
}

output_irq_bind()
{
    netQueueCount=`cat /proc/interrupts  | grep -i ".*virtio.*input.*" | wc -l`
    irqSet=`cat /proc/interrupts  | grep -i ".*virtio.*output.*" | awk -F ':' '{print $1}'`
    i=0
    for irq in $irqSet
    do
        cpunum=$((i%gCpuCount+1))
        mask=`get_smp_affinity_mask $cpunum`
        echo $mask > /proc/irq/$irq/smp_affinity
        echo "[output]bind irq $irq with mask 0x$mask affinity"
        ((i++))
    done
}

ethConfig()
{
    ethSet=`ls -d /sys/class/net/eth*`
    if ! command -v ethtool &> /dev/null; then
        source /etc/profile
    fi

    ethtool=`which ethtool`

    for ethd in $ethSet
    do
        eth=`basename $ethd`
        pre_max=`$ethtool -l $eth 2>/dev/null | grep -i "combined" | head -n 1 | awk '{print $2}'`
        cur_max=`$ethtool -l $eth 2>/dev/null | grep -i "combined" | tail -n 1 | awk '{print $2}'`
        # if ethtool not work. we have to deal with this situation.
        [[ ! "$pre_max" =~ ^[0-9]+$ ]] || [[ ! "$cur_max" =~ ^[0-9]+$ ]] && continue

        if [ $pre_max -ne $cur_max ]; then
            $ethtool -L $eth combined $pre_max
            echo "Set [$eth] Current Combined to <$pre_max>"
        fi
    done
}

smartnic_bind()
{
    irqSet=`cat /proc/interrupts  | grep "LiquidIO.*rxtx" | awk -F ':' '{print $1}'`
    i=0
    for irq in $irqSet
    do
        cpunum=$((i%gCpuCount+1))
        mask=`get_smp_affinity_mask $cpunum`
        echo $mask > /proc/irq/$irq/smp_affinity
        echo "[smartnic]bind irq $irq with mask 0x$mask affinity"
        ((i++))
    done
}

# return 0: yes, I'm a kvm vm
# return 1: no, I'm not
is_kvm_vm()
{
    local ret1
    local ret2

    # For ARM, ARM device not modelname
    archtype=`lscpu  | grep Architecture | awk '{print $2}'`
    if [ $archtype == "aarch64" ];then
        sys_vendor=`cat /sys/class/dmi/id/sys_vendor`
        chassis_vendor=`cat /sys/class/dmi/id/chassis_vendor`

        if [[ $sys_vendor == "Tencent Cloud" ]] || [[ $chassis_vendor == "QEMU" ]];then
            return 0
        else
            return 1
        fi
    fi

    # Quirk for 2080ti:
    #    We added a kvm:off parameter in qemu command line.
    #    This parameter hidden all kvm related featrues in vm,
    #    such as cpu tag and kvm clock source.
    #
    #    We passthough 2080ti function 0(vga) to vm only,
    #    So if there is 2080ti vga without function 1(audio),
    #    We know it is in vm enviroment.
    local vga=$(lspci -d 10de:1e04)
    local audio=$(lspci -d 10de:10f7)

    if [ "$vga" != '' ] && [ "$audio" == '' ]; then
        return 0
    fi

    # For ARM CVM. Cpu model name would be masked.
    local modelname=$(cat /proc/cpuinfo |grep "model name"|awk -F':' '{print $2}'|uniq|head -n 1)
    local modelname="${modelname#"${modelname%%[![:space:]]*}"}"
    [ -z "$modelname" ] && return 0
    [ "$modelname" == "Virtual" ] && return 0

    lscpu 2>/dev/null | grep -i kvm | grep -i Hypervisor >/dev/null 2>&1
    ret1=$?

    cat /sys/devices/system/clocksource/clocksource0/available_clocksource 2>/dev/null  | grep -i kvm >/dev/null 2>&1
    ret2=$?

    if [ "$ret1" == "0" -o "$ret2" == "0" ];then
        return 0
    else
        return 1
    fi
}

# return 0: yes shuishan bm
# return 1: not shuishan
is_shuishan()
{
    virtionum=`cat /proc/interrupts  | grep -i ".*virtio.*input.*" | wc -l`
    if [ $virtionum == 0 ]; then
        return 1
    else
        return 0
    fi
}

set_vm_net_affinity()
{
    ps ax | grep -v grep | grep -q irqbalance && killall irqbalance 2>/dev/null
    cat /proc/interrupts  | grep "LiquidIO.*rxtx" &>/dev/null
    if [ $? -eq 0 ]; then #smartnic
        echo "SET VM RSS SMARTNIC"
        smartnic_bind
    else
        ethConfig
        local cpuarch=`lscpu|grep Architecture|awk '{print $2}'`
        if [ "$cpuarch" == "aarch64" -a\
             "$gCpuCount" == 120 -a\
             -f $dir/armvirt120c_set_irqaffinity.sh ];then #ARM64 120C spec#
            echo "SET VM RSS AARCH64 120C spec.."
            $dir/armvirt120c_set_irqaffinity.sh
            return 
        fi
        echo "SET VM RSS NORMAL"
        #X86 and ARM64 other#
        input_irq_bind
        output_irq_bind
    fi
}

set_eth_bm_net_affinity()
{
    if [ $gCpuCount -ge 32 ]; then
        aff=$((gCpuCount-1))
        for i in $(awk -F ":" '/eth0/{print $1}' /proc/interrupts)
        do
            echo $aff > /proc/irq/$i/smp_affinity_list
            echo "$aff > /proc/irq/$i/smp_affinity_list"
            aff=$((aff-1))
            [ $aff == 0 ] && aff=$((gCpuCount-1))
        done
    else
        aff=1
        for i in $(awk -F ":" '/eth0/{print $1}' /proc/interrupts)
        do
            echo $aff > /proc/irq/$i/smp_affinity
            echo "$aff > /proc/irq/$i/smp_affinity"
            aff=$(echo "ibase=16;obase=10;$aff*2"|bc)
        done
    fi
}

set_virtio_bm_net_affinity()
{
    input_irq_bind
    output_irq_bind
}

set_bm_net_affinity()
{
    if [ $gCpuCount == 0 ];then
        echo cpunumber error
        return
    fi

    is_shuishan
    if [ $? -ne 0 ]; then
        ethConfig
        set_eth_bm_net_affinity
    else
        ethConfig
        set_virtio_bm_net_affinity
    fi
}

reverse_irq_for_nvme()
{
    lspci -nn | grep -q "Non-Volatile memory controller"
    [ $? == 0 ] && gReverse=1 || gReverse=0
}


# return 0: yes sa3 and cpu >= 128
# return 1: not
is_sa3_cross_node()
{
    milan=0
    cross_node=0
    is_milan=`cat /proc/cpuinfo | awk '{FS=":";if (NR==5) {print $2}}' | grep "AMD EPYC 7K83 64-Core Processor"`
    cpu_num=`cat /proc/cpuinfo | grep processor |wc -l`

    echo "is_milan:$is_milan cpu_num:$cpu_num"

    if [ -n "${is_milan}" ];then
        milan=1
    fi

    if [ $cpu_num -ge 128 ];then
        cross_node=1;
    fi


    if [ $milan -eq 1 -a $cross_node -eq 1 ];then
        return 0
    else
        return 1
    fi
}



set_net_affinity()
{
    sa3_cross_node=0

    is_sa3_cross_node

    if [ $? -eq 0 ]; then
        sa3_cross_node=1
    fi

    if [ $gCpuCount -ge 32 -a $sa3_cross_node -ne 1 ]; then
        gReverse=1
    else
        reverse_irq_for_nvme
    fi
    is_kvm_vm
    if [ $? -ne 0 ];then
        set_bm_net_affinity
    else
        set_vm_net_affinity
    fi

}

gCpuCount=`cat /proc/cpuinfo |grep processor |wc -l`
if [ $gCpuCount -eq 0 ] ;then
    echo "machine cpu count get error!"
    exit 0
elif [ $gCpuCount -eq 1 ]; then
    echo "machine only have one cpu, needn't set affinity for net interrupt"
    exit 0
fi

set_net_affinity
