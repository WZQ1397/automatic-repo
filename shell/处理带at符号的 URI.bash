#!/bin/bash
# 文件名: git_pull_code.sh
# 描述：拉取 git 仓库代码脚本

CODE_DIR=/data/www/project/public          # 源代码目录
GIT_USER=sh%40domain.com                   # git 用户名
GIT_PASS=password                          # git 密码
GIT_URL=gitlab.domain.com/demo.git         # git 仓库地址
OWNER=www-data                             # HTTP 运行用户

if [ -d ${CODE_DIR} ]
then
    cd ${CODE_DIR} && git pull origin master
else
    cd ${CODE_DIR%/*} && git clone http://${GIT_USER}:${GIT_PASS}@${GIT_URL} ${CODE_DIR##*/}
fi

chown -R ${OWNER} ${CODE_DIR}