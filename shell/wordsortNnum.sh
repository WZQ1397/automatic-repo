#!/bin/bash  
if [ $# -ne 2 -a $# -ne 1 ] ;then  
        echo "usage: `basename $0 ` [n] input file "  
        echo  
        exit  
fi  
  
if [ $# -eq 1 ];then  
        I_TOP=10  
        I_FILE=$1  
fi  
  
if [ $# -eq 2 ];then  
        I_TOP=$1  
        I_FILE=$2  
fi  

tr -sc "[A-Z][a-z]"  "[\012*]"  < $I_FILE | tr  "[A-Z]"  "[a-z]"  | \  
sort  | uniq -c | sort  -k1 -n -r  |  \  
head -$I_TOP | nl  
