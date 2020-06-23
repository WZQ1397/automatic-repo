# 读取INI文件中某段
# METHOD 1 按行读取
index($0,"[mysql]")){
    print # 输出$0
    while ((getline var) > 0) {
        if (var ~ /\[.*\]/) {
            exit 
        }
    }
    print var
}
# index($0,substr) ==> 起始从1开始，返回值大于0是位置，0是未找到子串
# getline ==> 大于0: 读取到内容，等于0: 表示文件EOF, 小于0: 读取失败


# METHOD 2 按段落读取
BEGIN	{
    RS=""
    FS="["
}
/mysql/{
    print 
}