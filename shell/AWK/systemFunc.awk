# 设置自定义函数
function getContextFromArr(arr,len) {
    startpos=1
    while (startpos<len+1) {
        print arr[startpos++]""
    }
}
function hexToDigit(hexnum) {
    # typeof 判断变量数据类型
    if(typeof(hexnum)=="string" || typeof(hexnum)=="strnum"){
        # strtonum 把字符串数字转成十进制数，支持8进制和16进制
        return toupper(hexnum) " --> " strtonum(hexnum)+1.5
    }else{
        return "Value is "typeof(hexnum)
    }
}
function formatNum(hexnum) {
    # 数值隐式转换为字符串时，将根据CONVFMT的格式按照sprintf()的方式自动转换为字符串。默认值为”%.6g
    CONVFMT="%.6f"
    PREC=5
    print hexToDigit(hexnum)
}

BEGIN{
    # 设置随机种子
    srand();
    # 生成随机长度，rand()返回[0,1)之间的随机数
    len = int(rand()*10)
    demostr="this is awk 4.231"
    print len
    # 使用内置length函数
    print demostr" length: "length(demostr)
    # substr(主字符串,开始位置,截取长度)
    print substr(demostr,0,len)
    # split(主字符串,目标保存数组,分隔标识符) 这里按照空格来分割,每个子串放入数组arr中
    split(demostr,arr," ")
    # 调用自定义函数
    getContextFromArr(arr,length(arr))
    hexnum="0x3b2a"
    print formatNum(hexnum)
    formatNum(arr[length(arr)])
}
