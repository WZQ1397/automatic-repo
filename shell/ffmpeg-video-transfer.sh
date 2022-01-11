camera_ip="rtsp://192.168.1.124:15000/test_mouse.mp4"
video_file=1.mp4
while true;
do
count=$1
while [[ $count -gt 1 ]];
do
video_file=$count.mp4
ffmpeg -rtsp_transport udp -stimeout 4000000 -i "${camera_ip}" -ss 0 -t 30 -r 5 -map 0 -f stream_segment -segment_format mpegts -segment_time 30 -segment_atclocktime 1 -reset_timestamps 1 -preset ultrafast -strftime 1 "${video_file}" &
count=$(($count-1))
done
ffmpeg -rtsp_transport udp -stimeout 4000000 -i "${camera_ip}" -ss 0 -t 30 -r 5 -map 0 -f stream_segment -segment_format mpegts -segment_time 30 -segment_atclocktime 1 -reset_timestamps 1 -preset ultrafast -strftime 1 "${video_file}"
done
