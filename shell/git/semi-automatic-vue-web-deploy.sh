# Author: zach.wang
version=$1
if [[ $version == "" ]];
then
   echo "Usage: $0 [version]"
   exit
fi
mkdir -pv web-backup/`date +%Y%m%d`/$version
cp -rv web/* web-backup/`date +%Y%m%d`/$version
rm -rf dist*
rz
unzip dist.zip
rm -rf web/$version/*
mv -v dist/* web/$version/
cat web/config.js.$version  > web/$version/config.js

