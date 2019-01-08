#!/bin/bash
cd /git_repo/salt_sls_repo
git add *
git commit -m "salt_`date +%Y%M%d`"
git log --graph
