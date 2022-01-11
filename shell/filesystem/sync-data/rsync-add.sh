#!/bin/bash
#Author Zach.Wang

#src ip 
S4="
news.lenchy.com
mc.szlawyers.com
szlawyer.lsxh.homolo.net
"
S5="
lg.lawyers.org.cn
lawfirms.lawyers.com.cn
www.lawyers.org.cn
"
S6="
mc.gzlawyer.org
video.gzlawyer.org
solr02.openlaw.cn
"

#command var
CMD="rsync -azvP"
src_data="/data/backup/"
dst_data=""
if [ dst_data -eq "" ];
then
	dst_data=$src_data
fi
if [ !-d $dst_data ];
then
	mkdir -pv $dst_data
fi

subfix="tsjinrong.top"


#### exec function ####

function check_rsync()
{
$name=$1
$site=$2
DATABASE="$(find $src_data/$site.$subfix/$name/database/*   -mtime  1)"
if [ ! -n "$DATABASE" ];then
	echo "没有发现"
else
	rm -rf $DATABASE
	echo "已经删除"
fi

}
function dir_exists()
{
	dir=$1
	if [ !-d $dir ];
	then
		mkdir -pv $dir
	fi
}

function rsync_fun()
{
	sync_logname=$1
	dir_exists $dst_data
	dir_exists $dst_data/synclogs
	$CMD s$i:$src_data  $dst_data/s$i.$subfix/ >> $dst_data/synclogs/$sync_logname.log
	
}

for ((i=4;i<7;i++))
   do
     eval value=\${S${i}[@]}
      for element in ${value}
         do
		   rsync_fun ${element}
           check_rsync ${element} S$i
          #continue 2
          #break
         done
    done
echo


