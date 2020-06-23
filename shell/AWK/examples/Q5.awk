# 去除注释中的内容
index($0,"/*"){
    if (index($0,"*/")) { # 同1行情况
        print gensub("^(.*)/\\*.*\\*/(.*)$","\\1\\2","g",$0)
    }else{ # 不同行情况
        # 输出/*后内容
        print gensub("^(.*)/\\*.*","\\1","g",$0)
        # 继续读取,直到*/结束符结束
        while ((getline var)>0) {
            if (index(var,"*/")) {
                print gensub("^.*\\*(.*)","\\1","g",var)
                break
            }
        }
    }
}
!index($0,"/*"){
    print 
}