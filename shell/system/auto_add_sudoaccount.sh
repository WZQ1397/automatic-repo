#!/bin/bash
USER=test
PASS=$USER
GROUP=root
HOME=/data/home/$USER
# if user not exist
if [[ $(cat /etc/passwd | grep -E '^$USER:' -c) == "0" ]]; then
  # use weak password
  sed 's/^password    requisite.*/password    requisite     pam_cracklib.so try_first_pass retry=3   type=/g' -i /etc/pam.d/system-auth
  # add user
  groupadd $GROUP 2>/dev/null
  mkdir -p /data/home && useradd $USER -d $HOME -g $GROUP
  # add sudo privilege
  sed '/$USER ALL=(ALL) NOPASSWD:ALL/d'  -i /etc/sudoers
  echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
  # set password
  passwd $USER << EOM
$PASS
$PASS
EOM
fi
