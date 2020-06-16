# 输出awk进程的内部信息，但跳过数组
# isarray(var)：测试var是否是数组，返回1(是数组)或0(不是数组)
# typeof(var)：返回var的数据类型，有以下可能的值：
    # “array”：是一个数组
    # “regexp”：是一个真正表达式类型，强正则字面量才算是正则类型，如@/a.*ef/
    # “number”：是一个number
    # “string”：是一个string
    # “strnum”：是一个strnum，参考strnum类型
    # “unassigned”：曾引用过，但未赋值，例如”print f;print typeof(f)”
    # “untyped”：从未引用过，也从未赋值过
BEGIN{
    for(idx in PROCINFO){
      if(typeof(PROCINFO[idx]) == "array"){
        continue
      }
      print idx " -> "PROCINFO[idx]
    }
  }