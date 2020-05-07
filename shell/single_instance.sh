#! /bin/bash

source /etc/profile

readonly LOCKFILE="/var/run/single_instance.pid"
readonly FD=$(ls -l /proc/$$/fd | sed -n '$p' | awk '{print $9}')
readonly LOCKFD=$(( ${FD}+1 ))

eexit() {
	local error_str="$@"
	echo -e ${error_str}
	exit 1
}

lock() {
	eval "exec ${LOCKFD}>${LOCKFILE}"
	flock -n ${LOCKFD} && echo "${BASHPID}" > "${LOCKFILE}" || eexit "\e[1;31m$0 is already running\x1b[0m"
}

unlock() {
	flock -u ${LOCKFD}
	eval "exec ${LOCKFD}>&-"
}

do_something() {
	sleep 20
	return 0
}

lock
do_something
if [[ $? == 0 ]]; then
	echo success
	unlock
else
	echo failed
fi