#!/bin/bash
git config --global user.name "zach"
git config --global user.email "wzqsergeant@vip.qq.com"
git config --global wzq1397.stack1 "saltstack1"
cat .gitconfig
mkdir -pv /git_repo/salt_sls_repo ; chmod 755 /git_repo/salt_sls_repo
cd /git_repo/salt_sls_repo/
git init
git status
