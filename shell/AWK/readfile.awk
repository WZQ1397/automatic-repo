function readfile(file    ,rs_bak,data){
  rs_bak=RS
  RS="^$"
  if ( (getline data < file) < 0 ){
    print "read file failed"
    exit 1
  }
  close(file)
  RS=rs_bak
  return data
}

/^1/{
  print $0
  content = readfile("z.awk")
  print content
}