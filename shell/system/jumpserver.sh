#!/bin/bash
####################################
echo "this is salt master"
echo "choose server follow"
echo "(1) localhost"
echo "(2) salt2"
echo "(q) exit!!!"
####################################

while [ True ];
do
	read -p "" choose
	case "$choose" in
		1) ssh salt1 && echo "you are on server `hostname`" ;;
		2) ssh salt2 && echo "you are on server `hostname`" ;;
		q) exit ;;
		*) echo "argv error!!!"
	esac
done
