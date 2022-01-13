choice=("hdd" "ram")
select=$1
delYes=$2
delYes=${delYes:-1}
success_select_content="Starting..."
failed_select_content="Usage: bash $0 [hdd|ram]"
config_path="/data/code/defect-tag-api-haoran/v2"
print_info=""
[[ ${choice[@]/${select}/} != ${choice[@]} ]] && print_info=$success_select_content || print_info=$failed_select_content
if [[ "$print_info" == "$failed_select_content" ]];
then
   exit -1
fi
keys=`echo $select| tr [a-z] [A-Z]`
sed -i "s/CAMERA_AUTO_MOVE_PATH_CHOICE = \".*\"/CAMERA_AUTO_MOVE_PATH_CHOICE = \"$keys\"/g" $config_path/settings.py
supervisorctl restart apiv2
for item in ${choice[@]};
do
   systemctl stop syncflow-${item}disk.service
   systemctl stop delOnehourAgoData-${item}disk.service
done
systemctl start syncflow-${select}disk.service
if [[ $delYes -eq 1 ]];
then
   systemctl start delOnehourAgoData-${select}disk.service
fi
