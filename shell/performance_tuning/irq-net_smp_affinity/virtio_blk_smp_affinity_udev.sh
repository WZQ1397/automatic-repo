#!/bin/bash

# Restore IRQ affinity setup when a virtio-blk device with multiple
# queues is plugged.
#
# It will first look for the saved affinity setup in
# /tmp/virtio_blk_saved_affinity.
# - If the setup does exist, it will setup the IRQ affinity of the
#   newly plugged virtio-blk device accordingly.
#
# - If the file does not exist, it will look for vcpus to which no
#   other multiple queue virtio-blk device has been bound. If such
#   cpus are found, it will bind IRQs of the newly plugged virtio-blk
#   device to that cpu. At most `nr_vqs_per_cpu` IRQs of a virtio-blk
#   device will be bound to one cpu. Otherwise, an error will be
#   reported and logged.
#
# /tmp/virtio_blk_saved_affinity is created and updated by the script
# virtio_blk_smp_affinity.sh and in a form like
#    virtio1 1 2
#    virtio2 3 4
# which means IRQs of virtio1 are bound to CPUs 1 and 2, and IRQs of
# virtio2 are bound to CPUs 3 and 4.
#
# All logs including error logs of this script is saved in
# /tmp/virtio_blk_affinity_udev.log.

lock_file="/tmp/virtio_blk_affinity_udev.lock"
saved_file="/tmp/virtio_blk_saved_affinity"
log_file="/tmp/virtio_blk_affinity_udev.log"

# `nr_vqs_per_cpu` specifies the amount of virtqueues of a virtio-blk
# device that can be bound to one cpu.
#
# Its value should be identical to `nr_vqs_per_cpu` in
# virtio_blk_smp_affinity.sh.
nr_vqs_per_cpu=1

# is_mq_virtio_blk(dev) checks whether `dev` (e.g., /dev/vda) is a
# virtio-blk device with multiple queues.
#
# Return 1 if it is; return 0 otherwise.
is_mq_virtio_blk()
{
	local dev_name=`basename $1`

	local sysfs="/sys/block/$dev_name"
	if [[ ! -d $sysfs && ! -L $sysfs ]]; then
		return 0
	fi

	local device_id=`cat $sysfs/device/device 2>/dev/null`
	local vendor_id=`cat $sysfs/device/vendor 2>/dev/null`
	if [[ ! $device_id -eq "0x0002" || ! $vendor_id -eq "0x1af4" ]]; then
		return 0
	fi

	if [[ ! -d "$sysfs"/mq ]]; then
		return 0
	fi

	local nr_queues=`ls -l "$sysfs"/mq | grep -c ^d`
	if [[ $nr_queues -le 1 ]]; then
		return 0
	fi

	return 1
}

# get_other_mq_virtio_blk_devices(dev) gets a list of all virtio-blk
# devices with multiple queues (e.g, "virtio1 virtio2 virtio3") except
# `dev` (e.g., /dev/vda).
#
# Exit 1 if any error occurs.
get_other_mq_virtio_blk_devices()
{
	local cur_dev_name=`basename $1`
	local other_devs=()

	for ent in /sys/block/*; do
		if [[ $cur_dev_name == `basename $ent` ]]; then
			continue
		fi

		if [[ ! -d $ent && ! -L $ent ]]; then
			echo "Skip $ent: not a directory or symbol link" >&2
			continue
		fi

		is_mq_virtio_blk $ent
		if [[ ! $? -eq 1 ]]; then
			echo "Skip $ent: not mq virtio-blk device" >&2
			continue
		fi

		local dev_name=`readlink "$ent"/device`
		dev_name=`basename "$dev_name"` || \
			{ \
			  echo "Error: failed to get the device name of $ent" >&2; \
			  exit 1; \
			}

		other_devs+=($dev_name)
	done

	echo ${other_devs[@]}
}

# smp_affinity_include_cpu(cpu_idx, affinity) checks whether cpu
# `cpu_idx` is included in the smp_affinity `affinity`.
#
# Return 1 if included; return 0 otherwise.
smp_affinity_include_cpu()
{
	local cpu_idx=$1
	local seg=$((cpu_idx/32))
	local oft=$((cpu_idx%32))

	local affinity=()
	IFS=',' read -ra affinity <<< `echo $2`
	local nr_segs=${#affinity[@]}

	if [[ $seg -ge $nr_segs ]]; then
		return 0
	fi
	seg=$((nr_segs - seg - 1))

	local affinity_seg="0x${affinity[$seg]}"
	local result=$(((1 << oft) & affinity_seg ))
	if [[ $result -ge 1 ]]; then
		return 1
	else
		return 0
	fi
}

# is_bound_to_cpu(dev, cpu_idx, full_affinity_mask) checks whether a
# virtio device `dev` is bound to cpu `cpu_idx`.
#
# Return 1 if bound; return 0 otherwise.
is_bound_to_cpu()
{
	local dev_name=$1
	local cpu_idx=$2
	local full_affinity_mask=$3
	local irqs=`cat /proc/interrupts | grep "$dev_name.req*" | awk -F ':' '{print $1}'`

	for irq in $irqs; do
		local affinity=`cat /proc/irq/$irq/smp_affinity`

		if [[ $affinity == $full_affinity_mask ]]; then
			continue
		fi

		smp_affinity_include_cpu $cpu_idx $affinity
		if [[ $? -eq 1 ]]; then
			return 1
		fi
	done

	return 0
}

# get_full_affinity_mask(nr_cpu) gets a smp_affinity mask that masks
# all `nr_cpu` cpus.
get_full_affinity_mask()
{
	local nr_cpus=$1
	local oft=$((nr_cpus%32))
	local segs=$((nr_cpus/32))

	local mask=""
	if [[ $oft -eq 0 ]]; then
		mask="ffffffff"
		segs=$((segs - 1))
	else
		mask=`printf "%x" $(((1 << oft) - 1))`
	fi

	while [[ $segs -gt 0 ]]; do
		mask+=",ffffffff"
		segs=$((segs - 1))
	done

	echo $mask
}

# get_free_cpus(dev, nr_required) searchs for `nr_required` cpus which
# are not used by all mq virtio-blk devices other than `dev` (e.g.,
# /dev/vda).
#
# If no error occurs, return an non-empty cpu index list. Otherwise,
# return an empty string.
get_free_cpus()
{
	local cur_dev=$1
	local nr_required=$2
	local other_devs=""
	local nr_cpus=`cat /proc/cpuinfo | grep processor | wc -l`
	local last_cpu=$((nr_cpus - 1))
	local full_mask=`get_full_affinity_mask $nr_cpus`

	other_devs=`get_other_mq_virtio_blk_devices $cur_dev`
	if [[ ! $? -eq 0 ]]; then
		echo "Error: failed to get the list of mq virtio-blk devices" >&2
		exit 1
	fi

	local required_cpus=()
	local nr_found=0

	for cpu_idx in $(seq 1 $last_cpu); do
		local bound=0

		for other_dev in $other_devs; do
			is_bound_to_cpu $other_dev $cpu_idx $full_mask
			if [[ $? -eq 1 ]]; then
				bound=1
				break
			fi
		done

		if [[ $bound -eq 0 ]]; then
			required_cpus+=($cpu_idx)
			nr_found=$((nr_found+1))
		fi

		if [[ $nr_found -eq $nr_required ]]; then
			break
		fi
	done

	echo ${required_cpus[@]}
}

# get_virtio_dev_name(dev) gets the virtio name (e.g., "virtio0") of
# `dev` (e.g., "/dev/vda").
#
# Exit 1 if any error occurs.
get_virtio_dev_name()
{
	local dev=`basename $1`

	local sysfs="/sys/block/$dev/device"
	if [[ ! -f $sysfs && ! -L $sysfs ]]; then
		echo "Error: not found $sysfs" >&2
		exit 1
	fi

	local name=""
	name=`basename $(readlink $sysfs)`
	if [[ ! $? -eq 0 ]]; then
		echo "Error: failed to get the device name of $dev" >&2
		exit 1
	fi

	echo $name
}

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

# get_saved_affinity(dev_name) gets the affinity CPU indices of device
# `dev_name` (e.g., "virtio0") from the file `saved_file`.
#
# Exit 1 if any error occurs.
get_saved_affinity()
{
	local dev_name=$1
	local afifnity=""
	local revtval=0

	if [[ ! -f $saved_file ]]; then
		echo "Error: not fould $saved_file" >&2
		exit 1
	fi

	affinity=`grep $dev_name $saved_file`
	retval=$?

	if [[ $retval -eq 1 ]]; then
		echo "Error: not found $dev_name in $saved_file" >&2
		exit 1
	elif [[ ! $retval -eq 0 ]]; then
		echo "Error: failed to search for $dev_name in $saved_file" >&2
		exit 1
	fi

	echo $affinity | awk '{$1=""; print substr($0,2)}'
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
}

try_lock()
{
	(set -o noclobber; echo "locked" > "$lock_file") 2>/dev/null
	echo $?
}

{
	trap 'rm -f "$lock_file"' EXIT
	while [[ ! `try_lock` -eq 0 ]]; do
		sleep 0.25
	done

	date

	virtio_dev=$1

	is_mq_virtio_blk $virtio_dev
	if [[ ! $? -eq 1 ]]; then
		echo "Skip: $virtio_dev not virtio-blk device with multiple queues" >&2
		exit 0
	fi

	# We should make sure that max_sectors_kb of mq virtio-blk
	# devices is equal to that of host NVMe devices
	vbdev=${virtio_dev##"/dev/"}
	echo "set $vbdev's max_sectors_kb to 128"
	echo 128 >/sys/block/$vbdev/queue/max_sectors_kb

	virtio_dev_name=`get_virtio_dev_name $virtio_dev`
	if [[ ! $? -eq 0 ]]; then
		exit 1
	fi

	irqs=(`cat /proc/interrupts | grep "$virtio_dev_name.req*" | awk -F ':' '{print $1}'`)
	nr_irqs=${#irqs[@]}
	nr_required_cpus=$(((nr_irqs+nr_vqs_per_cpu-1)/nr_vqs_per_cpu))

	target_cpus=`get_saved_affinity $virtio_dev_name`
	if [[ ! $? -eq 0 ]]; then
		echo "Warn: failed to restore irq affinity from $saved_file, try to find a free cpu"

		target_cpus=`get_free_cpus $virtio_dev $nr_required_cpus`
		if [[ ! $? -eq 0 ]]; then
			echo "Error: failed to find a free cpu for $virtio_dev"
			exit 1
		fi
	fi

	dev_set_irq_affinity $virtio_dev_name $nr_irqs ${irqs[@]} $target_cpus
} >> "$log_file" 2>&1
