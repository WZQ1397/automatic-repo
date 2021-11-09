for x in `seq 1 90`;
do
   {
     echo "scale=5000000; 4*a(1)" | bc -l -q;
   }&
done
