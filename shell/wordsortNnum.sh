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


#tr -cs "[a-z][A-Z][0-9]" "\n" |\ 
#tr A-Z a-z | sort | uniq -c | sort -k1nr -k2 | head -n $count
#tr是sed的简化，-c用前字符串中字符集的补集替换成后字符串即将不是字符和数字的单词替换换行
