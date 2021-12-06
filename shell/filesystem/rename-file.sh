id=1
for x in `ls | grep -v .sh`;
do
  new_filename=`seq -f "%05g" $id $id`".png"
  echo $x "==>" $new_filename;
  mv $x $new_filename
  id=$(($id+1))
done

