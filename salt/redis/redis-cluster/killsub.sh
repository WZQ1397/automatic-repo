for x in `ps aux | grep redis | grep -Ev "/usr/bin|grep" | awk '{print $2}'`
do
	kill $x
done