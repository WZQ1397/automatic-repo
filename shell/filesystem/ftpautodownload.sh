#!/usr/bin/ksh

############################################################
## 功能：从存储服务器获取确认文件
############################################################

#------------------------参数说明----------------------------
#--接收
#   localPath         -本地文件路径
#   remotePath        -远程文件路径
#   serverIP          -远程服务器IP
#   sftpUser          -sftp用户名
#   sftpPass          -sftp密码
#--变量
#   SYSDATE           -系统日期
#   STATION_ARR[]     -小站文件夹数组，新增小站增加此数组即可
#-----------------------------------------------------------

# 接收参数
localPath=$1
remotePath=$2
serverIP=$3
sftpUser=$4
sftpPass=$5

# 定义变量
SYSDATE=`date +%Y%m%d`
STATION_ARR[0]="k0001"
STATION_ARR[1]="k0253"
STATION_ARR[2]="zdfile"


#-----------------------------------------------------------
#--返回值RETURNCODE
#   0         -成功
#   1         -参数传递异常
#   2         -处理文件夹异常
#   3         -获取文件异常
#-----------------------------------------------------------

# [函数]脚本执行返回值
retrunCode()
{
    if [ ${result} -eq "1" ]; then
        RETURNCODE=$1
        echo ${RETURNCODE}
    fi
}

# [函数]处理日期文件夹
createForlder()
{
    cd $1
    if [[ ! -d ${SYSDATE} ]]; then
        mkdir ${SYSDATE}
        chmod 755 ${SYSDATE}
    fi
    cd ${SYSDATE}
}

# [函数]SFTP非交互式操作
sftp_download()
{
    expect <<- EOF
    set timeout 5
    spawn sftp $1@$2
    expect {
        "(yes/no)?" {send "yes\r"; expect_continue}
        "password:" {send "$3\r"}
    }
    expect "sftp>"
    send "cd $4\r"
    set timeout -1
    expect "sftp>"
    send "mget *$sysdate*04.*\r"
    expect "sftp>"
    send "mget *$sysdate*06.*\r"
    expect "sftp>"
    send "bye\r"
    EOF
}

# 校验参数个数
if [[ $# != 5 ]]; then
    exit
fi
result=$?
retrunCode "1"

# 处理文件夹
createForlder ${localPath}
result=$?
retrunCode "2"

# 循环获取文件
for station in ${STATION_ARR[@]}; do
    remoteDir=${remotePath}${station}
    sftp_download ${sftpUser} ${serverIP} ${sftpPass} ${remoteDir}
done
result=$?
retrunCode "3"