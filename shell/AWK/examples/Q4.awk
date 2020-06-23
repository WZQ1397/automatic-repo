# mktime("YYYY MM DD HH mm SS [DST]")
# systime()
# strftime(format,timestamp)

# 筛选指定时间范围内日志(指定开始时间,默认结束时间是现在)

# 格式1： "2019-11-10T03:45:13+08:00"
function strEpchoTime(timeStr) {
    patsplit(timeStr,"[0-9]{1,4}")
    Year=arr[1]
    Month=arr[2]
    Day=arr[3]
    Hour=arr[4]
    Minute=arr[5]
    Second=arr[6]
    return mktime("%s %s %s %s %s %s %s",Year,Month,Day,Hour,Minute,Second)
}

# 格式2： "10/Nov/2019:03:45:13+08:00"
function monthMap(mStr) {
    mM["Jan"]=1
    mM["Feb"]=2
    mM["Mar"]=3
    mM["Apr"]=4
    mM["May"]=5
    mM["Jun"]=6
    mM["Jul"]=7
    mM["Aug"]=8
    mM["Sep"]=9
    mM["Oct"]=10
    mM["Nov"]=11
    mM["Dec"]=12
    return mM[mStr]
}
function strEpchoTime2(timeStr) {
    dtStr= gensub("[/:+]"," ","g",timeStr)
    split(dtStr,arr," ")
    Year=arr[3]
    Month=monthMap(arr[2])
    Day=arr[1]
    Hour=arr[4]
    Minute=arr[5]
    Second=arr[6]
    return mktime("%s %s %s %s %s %s %s",Year,Month,Day,Hour,Minute,Second)
}

# 调用日志分析
BEGIN{
    str="2019-11-10T03:45:13+08:00"
    startTime=strEpchoTime(str)
}
{
    match($0,"^.*\\[(.*)]",nowTime)
    if (strEpchoTime(nowTime)>startTime) {
        print 
    }
}