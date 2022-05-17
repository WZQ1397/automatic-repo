#!/bin/bash -x 

echo "Jenkins Java Process"

cd /tmp
sudo find /proc -maxdepth 1 -user jenkins -type d -mmin +120 -exec basename {} \; | xargs ps | grep  maven3.agent ; :
sudo find /proc -maxdepth 1 -user jenkins -type d -mmin +120 -exec basename {} \; | xargs ps | grep maven3.agent | awk '{ print $1 }' | sudo xargs kill -9 ;:


echo "qa_bot Java Process"

sudo find /proc -maxdepth 1 -user qa_bot -type d -mmin +120 -exec basename {} \; | xargs ps | grep maven3.agent ;:
sudo find /proc -maxdepth 1 -user qa_bot -type d -mmin +120 -exec basename {} \; | xargs ps | grep maven3.agent | awk '{ print $1 }' | sudo xargs kill -9 ;:

sudo find /proc -maxdepth 1 -user qa_bot -type d -mmin +120 -exec basename {} \; | xargs ps | grep java | grep -v slave.jar ;:
sudo find /proc -maxdepth 1 -user qa_bot -type d -mmin +120 -exec basename {} \; | xargs ps | grep java | grep -v slave.jar | awk '{ print $1 }' | sudo xargs kill -9 ;:
