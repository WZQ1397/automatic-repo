#!/bin/bash
while getopts "A:D:L:P" opt; do
  case $opt in
    A)
      FUN=blockadd
      ;;
    D)
      FUN=blockdel
      ;;
    L)
      FUN=list
      ;;
    P)
      FUN=show_passwd
      ;;
    \?)
      echo "Invalid option: -$OPTARG"
      ;;
  esac
done
USERNAME=$2
NUM=$3
EXT_ARGS=$#

for(( l=4 ; l<=$EXT_ARGS ; l++ ))
do
        #printf "`eval '$'"$l"`"
        echo -e "${!l} \c" >> /tmp/vars
done
[ $EXT_ARGS -gt $l ] && ADD_ARGS=$(more /tmp/vars)
rm -rf /tmp/vars

[ ! -d /block_user ] && mkdir /block_user

blockadd()
{
        [ -f /etc/init.d/functions ] && source /etc/init.d/functions

        for(( list = 1 ; list <= $NUM ; list++ ))
        do
                id $USERNAME$list &> /dev/null
                USERchk=`echo $?`
                if [[ $USERchk -eq 0 ]];
                then
                                action "$USERNAME$list is exist!" /bin/false
                                continue
                fi
                pwd=$(echo $RANDOM | md5sum | cut -c 2-14 )
                #useradd $USERNAME$list && echo "$pwd" | passwd --stdin $USERNAME$list &> /dev/null
                useradd $USERNAME$list $ADD_ARGS && echo $USERNAME$list:$pwd | chpasswd &> /dev/null
                [ $? -eq 0 ] && action "OK! $USERNAME$list has added!" /bin/true
                echo -e "\033[32m "$USERNAME$list" \033[0m \t \033[31m "$pwd" \033[0m " | tee >> /block_user/$USERNAME-adduser.lst
                echo "`date +%F\" \"%T` created!" >> /block_user/$USERNAME-adduser.lst
        done
}

blockdel()
{
        [ -f /etc/init.d/functions ] && source /etc/init.d/functions

        for((list=1;list<=$NUM;list++))
        do
                id $USERNAME$list > /dev/null
                USERchk=`echo $?`
                if [[ $USERchk -eq 0 ]];
                then
                                userdel $USERNAME$list
                                [ $? -eq 0 ] && action "OK! $USERNAME$list has deleted!" /bin/true
                else
                                action "$USERNAME$list is not exist!" /bin/false
                                continue
                fi
                echo -e "\033[32m "$USERNAME$list" \033[0m" >> /block_user/$USERNAME-deluser.lst
                echo "`date +%F\" \"%T` deleted!" >> /block_user/$USERNAME-deluser.lst
        done
}

list()
{
        if [[ -d /block_user/ ]]
        then
                for lst in `ls /block_user/*user.lst`
                do
                        GRP_NAME=`ls $lst | awk -F "-" '{print $1}' | awk -F "/" '{print $NF}'`
                        echo -e " $GRP_NAME:\t $(grep -Ev "created|deleted" $lst | uniq | wc -l) "
                        tail -1 $lst
                        echo "==================="
                done
        else
                echo "There are no users add or database has cleared!"
        fi
}

show_passwd()
{
        grep -R $USERNAME /block_user | cut -d ":" -f 2
}

$FUN
