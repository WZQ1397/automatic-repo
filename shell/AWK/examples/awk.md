###### 1. 在字段a b c d后追加字段e f g

```awk
echo "a b c d" | awk '$2=$2" e f g"'
```

> 多个空格会合并成为一个空格,默认OFS=" "

###### 2. 从ifconfig的结果中选出非lo网卡的所有IP地址

```awk
# 按行匹配获取
ifconfig | awk '/inet/ && $2 !~ /^127|::1/{print $2}'
# 按段匹配获取
ifconfig | awk 'BEGIN{RS=""}!/^lo:/{print $6"-->"$12}'
```

> 修改RS值: RS="" 按段读取      RS="^$" 全部读取     RS="\n+" 按行读取
> 获取部分 NR(NUMBER ROW) ==> NR==1

###### 3. 根据某个字段去重

```awk
awk -F "?" '{arr[$2]++;if(arr[$2]==1){print}}' 1.txt
awk -F "?" '!arr[$2]++' 1.txt
```

###### 4. 处理丢失数据

```awk
BEGIN{FIELDWIDTHS="3 2:6 2:6 2:3 2:13"}NR==3{print $0}
```

> 2:6 表示跳过两个字符,此字段长度为6

###### 5. 处理含有分隔符的数据

```awk
echo "1,bob,male,\"page 37th,vail\",010-4324242"  # 数据
awk 'BEGIN{FPAT="[^,]+|\".*\""}{print $2,$4}'
```

###### 6. 取指定字段中内容前5个字符

```awk
echo "1,bob,male,\"page 37th,vail\",010-4324242"  # 数据
# 使用substr子串截取
awk -F "," '{print substr($2,1,5)}'
# 使用FIELDWIDTHS字段列宽来截取长度
awk -F "," 'FIELDWIDTHS="3 2:5" {print $2}'
```

###### 7. 对age字段(即$4)使用sort命令按数值大小进行排序

```awk
awk '
    BEGIN{
      CMD="sort -k4n";
    }

    # 将所有行都写进管道
    NR>1{
      print $0 |& CMD;
    }

    END{
      close(CMD,"to");  # 关闭管道通知sort开始排序
      while((CMD |& getline)>0){
        print;
      }
      close(CMD);
} ' a.txt
```