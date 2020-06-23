# 统计每个URL的独立IP访问IP有多少个（去重），并以URL为文件名保存 ???
BEGIN	{
    FS="#"
}
!urls[$1,$2]++{
    urls[$1]++
}
END	{
    for (i in urls) {
        # 保存文件重定向
        print i,"times: "urls[i] >(i".txt")
    }
}