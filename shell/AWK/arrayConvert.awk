BEGIN{
  arr["zhangsan"]=21
  arr["lisi"]=22
  arr["wangwu"]=23
  print a2s(arr)
}

function a2s(arr,content,i,cnt){
  for(i in arr){
    if(cnt){
      content=content""(sprintf("\t%s:%s\n",i,arr[i]))
    } else {
      content=content""(sprintf("\n\t%s:%s\n",i,arr[i]))
    }
    cnt++
  }
  return "{"content"}"
}