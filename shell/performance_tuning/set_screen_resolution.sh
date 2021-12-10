width=$1
height=$2
screen=$3
content=`cvt $width $height | tail -1` 
echo $content |  sed 's/Modeline/xrandr --newmode/g'
newmode_name=`echo $content | awk '{print $2}'`
echo "xrandr --addmode $screen $newmode_name"
echo "xrandr --output $screen --mode $newmode_name"

# xrandr | grep connected | awk '{print "OUTPUT DEIVCE: "$1}'
