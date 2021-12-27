script=$1
#for line in `cat $script` ;
cat $script |while read line; 
do 
   start=0
   line=($line)
   echo ${#line[*]}
   while [ $start -lt ${#line[*]} ];
   do
     echo ${line[$start]} | awk '{printf("%c", $1)}' >> $1.sh
     start=$(($start+1))
   done
   echo >> $1.sh
done 
