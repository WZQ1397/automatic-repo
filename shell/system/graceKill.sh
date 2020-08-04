pid=$1
count=$2
n=0
if [ ! -n $count ];then
    count=10
fi

while [[ $n  -lt  $count ]]
do
    let "n++"
    kill -0 $pid
    if [ $? -ne 0 ]
    then
        echo "program not exist"
        break
    else
        echo "send kill -15 to $pid"
	kill -15 $pid
        sleep 1
    fi
    if [[ $n  -eq $count ]]
    then
	echo "kill -9 $pid"
        # after 10s , try to send kill -9
	kill -9 $pid
    fi
done