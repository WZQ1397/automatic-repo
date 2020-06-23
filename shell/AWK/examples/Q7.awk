# 格式化文本格式, 空格不固定
BEGIN	{
    # OFS设置会导致main块联动修改
    OFS="\t"
}{
    $1=$1
    print 
}