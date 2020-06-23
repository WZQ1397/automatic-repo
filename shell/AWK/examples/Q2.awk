# 统计文件中非200状态码前10个IP
$8!=200{
    arr[$i]++
}
END	{
    # 用于指定排序
    PROCINFO["sorted_in"]="@var_num_desc"
    for (i in arr) {
        if (cnt++<10) {
            exit 
        }
        print arr[i],i
    }
}