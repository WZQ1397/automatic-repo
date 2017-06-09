#!/bin/bash
CorpID=wx703774c1a3da92e0
Secret=gobpQYLC-nY2aN4SuzLyvIAOpcDCwzHZ1mpQOUTR3L2jW2-s9Aqa50N7tCxuWJ3K
GURL="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$CorpID&corpsecret=$Secret"
Gtoken=$(/usr/bin/curl -s -G $GURL | awk -F\" '{print $4}')
PURL="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=$Gtoken"
function body() { 
                local int AppID=1
		local UserID=$1
		local PartyID=2
		 local Msg=$(echo "$2""\n""$3")
		#local Msg2=$(echo "$@"|awk '{print $3}')
	        #local msg=$(echo "$@" | cut -d" " -f3-)	
		cat << EOF
{
	"touser": "$UserID",
	"toparty": "$PartyID",
	"msgtype": "text",
	"agentid": " $AppID ",
	"text": {
		"content": "$Msg",
		},
	"safe":"0",
}
EOF
}
#echo "$(body "$1" "$2")" >> /tmp/wechat.log
/usr/bin/curl --data-ascii "$(body "$1" "$2" "$3")" $PURL
