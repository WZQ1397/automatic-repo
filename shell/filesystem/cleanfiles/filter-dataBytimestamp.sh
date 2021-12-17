 mypath=$1 # "20211213_TBC11HP_17_1639378477-1639378670"
  prefix="filter"
   newpath=$prefix"-"$mypath
   ORIPATH=$mypath # "20211213_TBC11HP_17_1639378477-1639378670"
   mkdir -pv $newpath
   echo $ORIPATH $newpath
   mypath=`echo $mypath | awk -F '_' '{print $NF}'`
   echo $mypath | awk -v ORIPATH=$ORIPATH -v newpath=$newpath -F '-' '{start=$(NF-1);end=$NF } END{for(;start<=end;start++){printf("start:%s ==> end:%s\n",start,end);cmd="find "ORIPATH"/ -name " start"* -exec mv -v {} "newpath" \;"; print cmd; system(cmd)}}'
