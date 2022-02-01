#!/bin/bash

# Distribute IRQs of multiple-queue (mq) virtio-blk devices according
# to following assumptions and rules.
#
# Suppose
# - D# is the number of mq virtio-blk devices.
# - N# is the number of vNUMA nodes,
# - P# is the value of D#/N#,
# - All mq virtio-blk devices are indexed from 0 to (D#-1).
#
# Assumtpions:
# (A1) mq virtio-blk devices can be evenly distributed among vNUMA nodes
#      i.e., D# % N# == 0.
# (A2) The amount of online vCPUs in a vNUMA nodes is not less than
#      the amount of mq virtio-blk devices in that node.
# (A3) vCPUs in one vNUMA node all come from host CPUs in the same host
#      NUMA node.
# (A4) vCPUs in different vNUMA nodes always come from different host
#      NUMA nodes.
# (A5) There is at least one SPDK thread in every host NUMA node where
#      a vNUMA node sits.
#
# Rules:
# (R1) IRQs of virtio-blk devices P#*i ~ P#*(i+1)-1 are bound to vNUMA
#      node i, where 0 <= i < N#.
# (R2) IRQs of virtio-blk devices P#*i+j are all bound to vCPUs
#      in vNUMA node i, where 0 <= i < N# and 0 <= j < P#.
# (R3) IRQs from different virtio-blk devices are bound to different
#      sets of vCPUS.
# (R4) Each vCPUs should not be bound more than `nr_vqs_per_cpu` IRQs
#      of a virtio-blk device.


# `blk_devs` is a list of names of virio-blk devices,
# e.g., ('virtio1', 'virtio2')
blk_devs=()
# `numa_nodes` is a list of sysfs paths of numa nodes,
# e.g., ('/sys/devices/system/node/node0', '/sys/devices/system/node/node1')
numa_nodes=()
saved_file="/tmp/virtio_blk_saved_affinity"

# `nr_vqs_per_cpu` specifies the amount of virtqueues of a virtio-blk
# device that can be bound to one cpu.
#
# Its value should be identical to `nr_vqs_per_cpu` in
# virtio_blk_smp_affinity_udev.sh.
nr_vqs_per_cpu=1

# vbdevs is a list of names of virtio
# e.g. vdb, vdc
vbdevs=""

# get_smp_affinity_mask(cpu_idx) gets the smp_affinity mask that
# binds resource to CPU `cpu_idx`, e.g.,
#  1. `get_smp_affinity_mask 1` returns "2"
#  2. `get_smp_affinity_mask 32` returns "1,00000000"
get_smp_affinity_mask()
{
	local cpu_idx=$1
	local offset=$((cpu_idx%32))
	local segs=$((cpu_idx/32))
	local mask=`printf "%x" $((1<<offset))`

	while [[ $segs -ge 1 ]]; do
		mask+=",00000000"
		segs=$((segs-1))
	done

	echo $mask
}

# get_node_cpu_list(node) gets a list of CPUs on numa node `node`,
# e.g., `get_node_cpu_list "/sys/devices/system/node/node0"` returns "0 1 2 3 8 9 10 11".
get_node_cpu_list()
{
	local node=$1
	local ranges=()
	local cpus=()

	IFS=',' read -ra ranges <<< `cat $node/cpulist`
	for range in ${ranges[@]}; do
		local lo=-1
		local hi=-1

		IFS='-' read -r lo hi <<< `echo $range`
		if [[ $lo -gt $hi || $lo -eq -1 || $hi -eq -1 ]]; then
			echo "Error: failed to get CPU range on $node"
			exit 1
		fi

		cpus=(${cpus[@]} $(seq $lo $hi))
	done

	echo ${cpus[@]}
}

# Get a list of mq virtio-blk devices and save it in the variable `blk_devs`.
get_mq_virtio_blk_devices()
{
	blk_devs=()

	for ent in /sys/block/*; do
		if [[ ! -d $ent && ! -L $ent ]]; then
			echo "Skip $ent: not a directory or symbol link"
			continue
		fi

		if [[ $(is_virtio_blk $ent) -eq 0 ]]; then
			echo "Skip $ent: not a virtio-blk device"
			continue
		fi

		if [[ ! -d "$ent"/mq ]]; then
			echo "Skip $ent: not a mq device"
			continue
		fi

		local nr_queues=`ls -l "$ent"/mq | grep -c ^d`
		if [[ $nr_queues -le 1 ]]; then
			echo "Skip $ent: single queue device"
			continue
		fi

		local dev_name=`readlink "$ent"/device`
		dev_name=`basename "$dev_name"` || \
			{ \
			  echo "Error: failed to get the device name of $ent"; \
			  exit 1; \
			}

		# record all the vdx to a global variable
		vbdevs+=${ent##"/sys/block/"}
		vbdevs+=" "

		blk_devs+=($dev_name)
	done
}

# is_virtio_blk(dev) checks whether `dev` is a virtio-blk device, e.g.,
#  1. `is_virtio_blk "/sys/block/vda"` returns 1
#  2. `is_virtio_blk "/sys/block/sda"` returns 0
is_virtio_blk()
{
	local dev=$1
	local device_id=`cat $dev/device/device 2>/dev/null`
	local vendor_id=`cat $dev/device/vendor 2>/dev/null`

	if [[ $device_id == "0x0002" && $vendor_id == "0x1af4" ]]; then
		echo 1
	else
		echo 0
	fi
}

# update_saved_affinity(dev_name, cpus) logs the affinity between the
# virtio-blk device `dev_name` (e.g., virtio0, virtio1, etc.) and the
# vCPU `cpus` in the log file `saved_file`. If a line for `dev_name`
# has already existed, it will be updated. Otherwise, a new line will
# be added.
update_saved_affinity()
{
	local args=("$@")
	local dev_name=${args[0]}
	local line="${args[@]}"

	grep ^$dev_name $saved_file > /dev/null
	local found=$?
	if [[ $found -eq 1 ]]; then
		echo $line >> $saved_file
	elif [[ $found -eq 0 ]]; then
		sed -i -e "s/$dev_name.*/$line/g" $saved_file
	else
		echo "Error: failed when searching $dev_name in file $saved_file"
		exit 1
	fi
}

# alloc_cpu(pos, cpus) searches the CPU array `cpus` from the `pos`'th
# element (position starts from 0) for an online CPU.
#
# Returns the CPU id if found; otherwise, exit 1.
alloc_cpu()
{
	local args=("$@")
	local pos=${args[0]}
	local cpus=(${args[@]:1})
	local nr_cpus=${#cpus[@]}
	local cpu_idx=-1

	while [[ $pos -lt $nr_cpus ]]; do
		local idx=${cpus[$pos]}

		if [[ `cat /sys/devices/system/cpu/cpu$idx/online` -ne 1 ]]; then
			pos=$((pos+1))
			continue
		fi

		cpu_idx=$idx
		pos=$((pos+1))
		break
	done

	if [[ $cpu_idx -eq -1 ]]; then
		exit 1
	fi

	echo $cpu_idx
}

# dev_set_irq_affinity(dev_name, nr_irqs, irqs, cpus) sets
# the affinity of IRQs `irqs` of the virtio-blk device `dev_name` to
# CPUs `cpus`.
dev_set_irq_affinity()
{
	local args=("$@")
	local dev_name=${args[0]}

	local nr_irqs=${args[1]}
	local irqs=(${args[@]:2:$nr_irqs})

	local cpus=(${args[@]:$((2+nr_irqs))})

	local irqs_cnt=0
	local cpus_pos=0

	local cpu_idx=${cpus[$cpus_pos]}
	local mask=`get_smp_affinity_mask $cpu_idx`

	for irq in "${irqs[@]}"; do
		echo $mask > /proc/irq/$irq/smp_affinity
		if [[ "$?" -ne 0 ]]; then
			echo "Error: failed to set smp_affinity of irq $irq to $mask"
			exit 1
		fi
		echo "Info: set smp_affinity of irq $irq to mask $mask (cpu $cpu_idx)"

		irqs_cnt=$((irqs_cnt+1))
		if [[ $irqs_cnt -eq $nr_vqs_per_cpu ]]; then
			irqs_cnt=0
			cpus_pos=$((cpus_pos+1))
			cpu_idx=${cpus[$cpus_pos]}
			mask=`get_smp_affinity_mask $cpu_idx`
		fi
	done

	update_saved_affinity $dev_name ${cpus[@]}
}

# devs_set_irq_affinity() distributes IRQs of virtio-blk devices to
# different CPUs according to rules stated at the beginning of this
# script.
devs_set_irq_affinity()
{
	local dev_sidx=0

	for node in ${numa_nodes[@]}; do
		local cpus=(`get_node_cpu_list $node`)
		local next_free_cpu_pos=0
		local dev_eidx=$((dev_sidx+nr_devs_per_node-1))

		for dev_idx in $(seq $dev_sidx $dev_eidx); do
			local dev_name=${blk_devs[$dev_idx]}
			local irqs=(`cat /proc/interrupts | grep "$dev_name.req*" | awk -F ':' '{print $1}'`)
			local nr_vqs=${#irqs[@]}
			local nr_required_cpus=$(((nr_vqs+nr_vqs_per_cpu-1)/nr_vqs_per_cpu))

			local required_cpus=()
			for i in $(seq 1 $nr_required_cpus); do
				local cpu_idx=0

				cpu_idx=`alloc_cpu $next_free_cpu_pos ${cpus[@]}`
				if [[ ! $? -eq 0 ]]; then
					echo "Error: failed to find a free online CPU on $node"
					exit 1
				fi

				# Skip CPU0 in hope to reduce its load
				if [[ $cpu_idx -eq 0 ]]; then
					next_free_cpu_pos=$((next_free_cpu_pos+1))
					cpu_idx=`alloc_cpu $next_free_cpu_pos ${cpus[@]}`
					if [[ ! $? -eq 0 ]]; then
						echo "Error: failed to find a free online CPU on $node"
						exit 1
					fi
				fi

				required_cpus+=($cpu_idx)
				next_free_cpu_pos=$((next_free_cpu_pos+1))
			done

			echo "$dev_name: cpus ${required_cpus[@]}, irqs ${irqs[@]}"
			dev_set_irq_affinity $dev_name $nr_vqs ${irqs[@]} ${required_cpus[@]}
		done

		dev_sidx=$((dev_eidx+1))
	done
}

get_mq_virtio_blk_devices
nr_blk_devs=${#blk_devs[@]}
if [ $nr_blk_devs -eq 0 ]; then
	echo "Skip: not found virtio-blk mq devices"
	exit 0
fi

echo "Info: found $nr_blk_devs virtio-blk mq devices: ${blk_devs[@]}"

# We should make sure that max_sectors_kb of mq virtio-blk
# devices is equal to that of host NVMe devices.
for vbdev in $vbdevs
do
	echo "set $vbdev's max_sectors_kb to 128"
	echo 128 >/sys/block/$vbdev/queue/max_sectors_kb
done

numa_nodes=(`find /sys/devices/system/node/ -mindepth 1 -type d -name "node*"`)
nr_nodes=${#numa_nodes[@]}
if [[ $nr_nodes -eq 0 ]]; then
	echo "Error: failed to get the numa node information"
	exit 1
fi
if [[ $((nr_blk_devs%nr_nodes)) -ne 0 ]]; then
	echo "Error: $nr_blk_devs virtio-blk devices cannot be evenly distributed to $nr_nodes nodes"
	exit 1
fi
nr_devs_per_node=$((nr_blk_devs/nr_nodes))

echo "Info: found $nr_nodes numa nodes: ${numa_nodes[@]}"
echo > $saved_file

devs_set_irq_affinity
