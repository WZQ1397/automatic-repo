#!/bin/bash

FSID="1"
EXPORT_DIR="/nfs"         
EXPORT_OPTIONS="-o rw,sync,all_squash,annonuid=65534,annongid=65534,mp,fsid=$FSID"
EXPORT_CLIENT="192.168.1.0/24"

exportfs_usage() {
cat <<EOF
    USEAGE: $0 {start|stop}
EOF
}

exportfs_start()
{
    fn="/nfs"
    service rpcbind stop &>/dev/null
    service rpcbind start  &>/dev/null
    service nfs restart  &>/dev/null
        echo "=======nfs restart========"
    exportfs ${EXPORT_OPTIONS} ${EXPORT_CLIENT}:${EXPORT_DIR} 2>1&    #通过exportfs来申明共享目录
    rc=$?
    if [ $rc -ne 0 ];then
        echo "export resource ${EXPORT_DIR} error"
        exit $rc
    else
            echo "export resource ok"
        exit 0
    fi
}

exportfs_stop()
{
    fn="/nfs"
    service rpcbind stop &>/dev/null
        service rpcbind start  &>/dev/null
    service nfs restart  &>/dev/null
        echo "=======nfs restart========"
    exportfs -u  ${EXPORT_CLIENT}:${EXPORT_DIT} 2>1&   通过exportfs来取消共享目录
    rc=$?
    if [ $rc -ne 0 ];then
        echo "export resource ${EXPORT_DIR} error"
        exit $rc
    else
            echo "umount ${EXPORT_DIR} ok"
        exit 0
    fi
}

if [ $# -lt 1 ];then
    exportfs_usage
    exit 1
fi
case $1 in
    start)
    exportfs_start
    ;;
    stop)
    exportfs_stop
    ;;
    *)
    exit 1
    ;;
esac