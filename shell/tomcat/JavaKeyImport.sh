#!/bin/bash

JAVA_HOME=/data/web/jdk1.7.0_71

keytool -import -trustcacerts -alias utssso -file /data/keys/1_root_bundle.crt -keystore $JAVA_HOME/jre/lib/security/cacerts  -storepass changeit

