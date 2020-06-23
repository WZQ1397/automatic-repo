# 行列转换
{
    for (i=1;i<=NF;i++) {
        if (i in arr) {
            arr[i]=arr[i]" "$i
        }else{
            arr[i]=$i
        }
    }
}
END	{
    for (i=1;i<=NF;i++) {
        print arr[i]
    } 
}