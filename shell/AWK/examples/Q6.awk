# 文件处理,现有两个文件,f1和f2各5列,用f2的第一列减去f1的第1列,把所得结果替换第五列内容(f2)
# METHOD 1
{
    f1=$1
    if((getline<"f2")>=0){
        $5 = $1-f1
        print $0
    }
}

# METHOD 2
NR==FNR{
    ARR[FNR]=$1
}
NR!=FNR{
    $5=$1-ARR[FNR]
    print $0
}

# awk -f Q6.awk f1 f2