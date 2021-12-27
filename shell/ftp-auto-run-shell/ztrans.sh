script=$1
> $1.txt
cat $script | while read line 
do 
   start=0
   end=$(($start+1))
   echo ${#line}
   while [ $end -le ${#line} ];
   do
     if [[ $end -eq ${#line} ]];
     then
       printf "%d" "'${line:$start:$end}" >> $1.txt
     else
       printf "%d " "'${line:$start:$end}" >> $1.txt
     fi
     start=$(($start+1))
     end=$(($start+1))
   done
   echo >> $1.txt
done 
