#!/bin/bash
arr=(
1080p
720p
3d
)
for category in $arr[*]
do
    for ((i=1;i<5;i++))
    do
        # Define return value
        RETURN=`curl -o /dev/null -s -k -w "%{http_code}" http://www.1080pdy.com/forum-$category-$i.html`
        if [ $RETURN -eq 200 ]; then
            # if return value 200,then flush page and category.
            curl -o /dev/null -s -k -w "%{http_code}" http://www.1080pdy.com/forum-$category-$i.html >/dev/null 2>&1
            curl -o /dev/null -s -k -w "%{http_code}" http://www.1080pdy.com/?r=y >/dev/null 2>&1
        else
            # if return value not 200,then flush category first page and site page.break
            curl -o /dev/null -s -k -w "%{http_code}" http://www.1080pdy.com/forum-$category-$i.html >/dev/null 2>&1
            curl -o /dev/null -s -k -w "%{http_code}" http://www.1080pdy.com/forum-$category-$i.html?r=y >/dev/null 2>&1
            break
        fi
    done
done
