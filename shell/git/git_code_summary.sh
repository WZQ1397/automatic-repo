#!/bin/bash
date_star='2020-02-01'
date_end='2020-03-30'
path1=`find /home/ops/gitlab/volume/data/git-data -name "*.git" | grep -v ".*wiki.git"`

arr=($path1)

for path in ${arr[@]};do
	project_name=`basename ${path} | cut -d'.' -f 1`
	cd ${path} && \
	git log --pretty='%aN' >> /dev/null 2>&1
	if [ $? -eq 0 ];then
		for user in `git log --pretty='%aN' | sort | uniq`;do
			cd ${path} && \
			for branch_a in `git branch -a| awk '{print $NF}'`;do
				code_branch_num=`git log ${branch_a} --since=$date_star --until=$date_end --author=${user} --pretty=tformat: --numstat | awk '{ loc += $1 -$2 } END { printf loc }'`
				if [ ! ${code_branch_num} ];then
					echo skip
				else
					echo ${project_name}_${user}_${branch_a}_${code_branch_num} >> /home/ops/total.txt
				fi
			done
		done
	fi
done

