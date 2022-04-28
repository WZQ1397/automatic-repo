#!/bin/bash
STAGE="$1"
filename="all.yml"
if [[ $STAGE == "PRD" ]];
then
   DOMAIN="usws00.com"
else
   filename="dev.yml"
   DOMAIN="uses01.com"
fi
echo $filename $DOMAIN
for myhost in `grep ": null" $filename | sed -e 's/^[ ]*//g' -e 's/: null//g'`;
do
  printf "\$CMD %s.%s\n" $myhost $DOMAIN
  #printf "\$CMD %s" $myhost
  #echo .$DOMAIN
done
