#####  删除1小时前数据
delOnehourAgoData.sh

```
/bin/bash delOnehourAgoData.sh 指定删除目录 删除多少分钟前的数据
EG: bin/bash /data2/save-data/delOnehourAgoData.sh /data2/save-data/camera/movePicFromMemDisk/camera 3
```

##### 切分最近1小时前日志文件
splitlast1wlog.sh

##### cleanCamRecordPicAndDBRecord 配套
sqlrunner.sql

##### 切换存储类型
swap_storage_type.sh

##### 同步数据
syncflow.sh
```
/bin/bash delOnehourAgoData.sh 源目录 目标目录
EG: /bin/bash /data2/save-data/syncflow.sh /data2/save-data/camera/movePicFromMemDisk/camera /data2/save-data/camera
```

##### 相机照片与数据库信息清理
```
/data2/save-data/tools/cleanCamRecordPicAndDBRecord -r 保留时间 -t 磁盘空间阈值 -s 开始相机ID -e 结束相机ID -p 清理路径
EG: /data2/save-data/tools/cleanCamRecordPicAndDBRecord -r 30 -t 85 -s 1 -e 9 -p /data/defect/staticv2/heatmap_path
```


